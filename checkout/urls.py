from django.urls import path

from checkout.views import checkout, checkout_success
from checkout.webhooks import webhook

urlpatterns = [
    path("", checkout, name="checkout"),
    path(
        "checkout_success/<order_number>",
        checkout_success,
        name="checkout_success",
    ),
    path("wh", webhook, name="webhook"),
]
