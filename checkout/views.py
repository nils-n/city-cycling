"""view function for the checkout app"""

import json

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

import stripe  # no qa

from checkout.forms import OrderForm, Order
from profiles.forms import UserProfileForm

from checkout.models import OrderLineItem
from products.models import Product


from bag.contexts import bag_contents
from icecream import ic

User = get_user_model()


@require_POST
def cache_checkout_data(request):
    """send metadata about the order to the frontend"""
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "save_info": request.POST.get("save_info"),
                "username": request.user,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "sorry, your payment could \
            not be processec right now. Please try again later",
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    ic("entering checkout view")
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get("bag", {})
        ic("this request is a POST request")

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            ic("OK the order form was valid")
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data[
                            "items_by_size"
                        ].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    ic("ERROR this product does not exist")
                    messages.error(
                        request,
                        (
                            "One of the products in your bag \
                                wasn't found in our database. "
                            "Please call us for assistance!"
                        ),
                    )
                    order.delete()
                    return redirect(reverse("view_bag"))
            ic("OK the order has been saved ")

            request.session["save_info"] = "save-info" in request.POST
            ic("OK returning now to checkout_success view ")
            ic(order.order_number)
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please double check your information.",
            )

    else:
        bag = request.session.get("bag", {})
        if not bag:
            messages.error(request, "There is nothing in your bag")
            return redirect(reverse("products"))

        current_bag = bag_contents(request)
        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total, currency=settings.STRIPE_CURRENCY
        )

        if request.user.is_authenticated:
            try:
                user_profile = User.objects.get(pk=request.user.id)
                # TC_21 : quirky way of passing flake8 line-too-long error
                # by adding noqa and decreasing line indent slightly.
                order_form = OrderForm(
                    initial={  # noqa
                        "full_name": user_profile.get_full_name(),  # noqa
                        "email": user_profile.email,  # noqa
                        "phone_number": user_profile.default_phone_number,  # noqa
                        "country": user_profile.default_country,  # noqa
                        "postcode": user_profile.default_postcode,  # noqa
                        "town_or_city": user_profile.default_town_or_city,  # noqa
                        "street_address1": user_profile.default_street_address1,  # noqa
                        "street_address2": user_profile.default_street_address2,  # noqa
                        "county": user_profile.default_county,
                    }
                )
            except User.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing.")

        template = "checkout/checkout.html"
        context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """Handle successful checkouts"""
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        """attach user profile to order"""
        user_profile = get_object_or_404(User, id=request.user.id)
        order.user_profile = user_profile
        order.save()

        if save_info or 1:
            # TC_21 : quirky way of passing flake8 line-too-long error
            # by adding noqa and decreasing line indent slighlty.
            profile_data = {  # noqa
                "default_phone_number": order.phone_number,  # noqa
                "default_country": order.country,  # noqa
                "default_postcode": order.postcode,  # noqa
                "default_town_or_city": order.town_or_city,  # noqa
                "default_street_address1": order.street_address1,  # noqa
                "default_street_address2": order.street_address2,  # noqa
                "default_county": order.county,
            }
            user_profile_form = UserProfileForm(
                profile_data, instance=user_profile
            )
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        f"Order successfully placed. \
            A confirmation email is being sent to {order.email}",
    )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/checkout_success.html"

    context = {"order": order}

    return render(request, template_name=template, context=context)
