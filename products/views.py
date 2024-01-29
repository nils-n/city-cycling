from icecream import ic
import json
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models.functions import Lower
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from products.models import Product, Category, ProductRating
from products.forms import ProductForm
from profiles.models import Comment  # noqa


def all_products(request):
    """view to display all products in the shop"""
    products = Product.objects.all()
    all_categories = Category.objects.all()
    categories = None
    sort = None
    direction = None
    categories = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
        if "direction" in request.GET:
            direction = request.GET["direction"]
            if direction == "desc":
                sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)
        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)

    else:
        # if no search criteria applied, display products from current season
        current_month = datetime.now().month
        # have to use a Q object to also account for the winter season
        products = products.filter(
            Q(
                season__start_month__lte=current_month,
                season__end_month__gte=current_month,
            )
            | Q(
                season__start_month__gte=current_month,
                season__end_month__gte=current_month,
                season__end_month__lte=3,
            )
            | Q(
                season__start_month__gte=11,
                season__end_month__lte=current_month,
            )
        )

    current_sorting = f"{sort}_{direction}"

    return render(
        request,
        "products/products.html",
        context={
            "products": products,
            "current_sorting": current_sorting,
            "all_categories": all_categories,
        },
    )


def product_detail(request, product_id):
    """view to display product detail in the shop"""
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.all()

    # load ratings of all users
    ratings = []
    for comment in comments:
        try:
            product_id = comment.object_id
            targeted_product = Product.objects.get(pk=comment.object_id)
            rating = ProductRating.objects.get(
                user=comment.user, product=targeted_product
            )
            # ratings are stored as decimals hence multi
            decimal_scaling_factor = 100
            ratings.append(decimal_scaling_factor * rating.value)
        except Exception:
            ratings.append("")

    number_of_reviews = sum([1 for rating in ratings if not ""])
    ic(number_of_reviews)

    # prepare a zipped list
    reviews = zip(comments, ratings)

    return render(
        request,
        "products/product_detail.html",
        context={
            "product": product,
            "reviews": reviews,
            "number_of_reviews": number_of_reviews,
        },
    )


@login_required
def add_product(request):
    """add a product to the store"""

    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product successfully added.")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to add product. Check if your form is valid."
            )
    else:
        form = ProductForm()

    template = "products/add_product.html"

    context = {"form": form}

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """edit a product in the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)

    if request.POST:
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product successfully edited.")
            return redirect(
                reverse(
                    "product_detail",
                    args=[product.id],
                )
            )
        else:
            form = ProductForm(instance=product)
            messages.error(
                request,
                "Faild to update Product.\
                 Have you entered the form correctly?",
            )

    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")

    template = "products/edit_product.html"

    context = {"form": form, "product": product}

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """delete a product form the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()

    messages.success(request, "Product successfully deleted.")

    return redirect(reverse("products"))


@login_required
def rate_product(request, product_id):
    """add rating to a purchased product
    based on  https://docs.djangoproject.com/en/5.0/ref/models/querysets/
    """

    post_data = json.loads(request.body.decode("utf-8"))

    if "rating" in post_data:
        rating = int(post_data["rating"])
        user_id = int(post_data["userId"])
        product_id = int(post_data["productId"])
        ic(rating, user_id, product_id)

        # ensure that the request has been sent by the same user
        if user_id == request.user.id:
            product = get_object_or_404(Product, pk=product_id)

            try:
                existing_rating = ProductRating.objects.get(
                    user=request.user, product=product
                )
                existing_rating.value = rating
                existing_rating.save()
                messages.success(request, "Rating successfully updated. ")
            except Exception:
                new_rating = ProductRating(
                    user=request.user, product=product, value=rating
                )
                new_rating.save()
                messages.success(request, "Rating successfully given. ")

            # update overall rating of the product
            # https://docs.djangoproject.com/en/5.0/topics/db/aggregation/
            avg_rating = ProductRating.objects.filter(
                product__id=product.id
            ).aggregate(Avg("value", default=0))
            product.rating = int(100 * int(avg_rating["value__avg"]))
            product.has_rating = True
            try:
                product.save()
                messages.success(request, "rating saved.")
            except Exception as e:
                messages.error(request, f"could not save rating. Error : {e}")

    return redirect(reverse("profile", args=(user_id,)))


@login_required
def comment_product(request, product_id):
    """add rating to a purchased product
    based on  Generic Foreign Keys in Django
    / GenericForeignKey / GenericRelation, see:
    https://www.youtube.com/watch?v=Wt4_7ZAE8dI
    """

    post_data = json.loads(request.body.decode("utf-8"))

    if "comment" in post_data:
        comment = post_data["comment"].lstrip()
        user_id = int(post_data["userId"])
        product_id = int(post_data["productId"])
        product = Product.objects.get(pk=product_id)

        ic(comment, user_id, product_id)
        # ensure that the request has been sent by the same user
        if user_id == request.user.id:
            ic(product.name)
            comments = Comment.objects.filter(
                product__name=product.name, user=request.user
            )
            # there is no comment in the database for this user, so create one
            if comments.count() == 0:
                new_comment = Comment.objects.create(
                    text=comment, content_object=product, user=request.user
                )
                new_comment.save()

            else:
                # there is already a comment, so update it now
                existing_comment = comments.first()
                existing_comment.text = comment
                existing_comment.is_approved = False
                existing_comment.save()

            # store info that product has comments
            product.has_comments = True
            try:
                product.save()
                messages.success(request, "comment saved.")
            except Exception as e:
                messages.error(request, f"could not save comment. Error : {e}")

    return redirect(reverse("profile", args=(user_id,)))
