from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import ProductRating
from profiles.forms import UserProfileForm
from profiles.models import Comment
from checkout.models import Order

User = get_user_model()


@login_required
def profile(request):
    """Display user profile
    https://learndjango.com/tutorials/django-best-practices-referencing-user-model
    """
    user_profile = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User Profile successfully updated.")
        else:
            messages.error(
                request, "Could not update user Profile. Is your form valid?"
            )
    else:
        form = UserProfileForm(instance=user_profile)

    orders = user_profile.orders.all()
    hide_bag_preview = True
    comments = Comment.objects.filter(user=request.user)

    from icecream import ic  # noqa

    # store the purchased products
    purchased_products = []
    for order in orders:
        for line_item in order.lineitems.all():
            product_id = line_item.product.id
            if product_id not in purchased_products:
                purchased_products.append(line_item.product)

    # store the user comments
    user_comments = []
    for product in purchased_products:
        try:
            comment = Comment.objects.get(
                user=request.user, object_id=product.id
            )
            user_comments.append(comment.text)
        except Exception:
            user_comments.append("")

    # store user ratings
    user_ratings = []
    for product in purchased_products:
        try:
            rating = ProductRating.objects.get(
                user=request.user, product=product
            )
            # ratings are stored as decimals hence multi
            decimal_scaling_factor = 100
            user_ratings.append(decimal_scaling_factor * rating.value)
        except Exception:
            user_ratings.append("")

    ic(user_ratings)

    # prepare a zipped list
    purchase_information = zip(purchased_products, user_comments, user_ratings)

    template = "profiles/profile.html"
    context = {
        "orders": orders,
        "form": form,
        "hide_bag_preview": hide_bag_preview,
        "purchase_information": purchase_information,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Display a past order to the user
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        f"This is a past confirmation for {order_number}. A confirmation Email was sent on the order date.",
    )

    template = "checkout/checkout_success.html"
    context = {"order": order, "from_profile": True}

    return render(request, template, context)
