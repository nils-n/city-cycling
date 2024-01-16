import os
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from checkout.forms import OrderForm


def checkout(request):
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There is nothing in your bag")
        return redirect(reverse("products"))

    order_form = OrderForm()
    template = "checkout/checkout.html"

    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": settings.STRIPE_SECRET_KEY,
    }

    return render(request, template, context)