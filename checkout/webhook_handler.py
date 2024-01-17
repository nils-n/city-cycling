from django.http import HttpResponse
from icecream import ic


class StripeWH_Handler:
    """Handle Stripe Webhooks (Event Signals)."""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic / unknown/ unexpected webhook event."""
        ic("handling a generic event")
        return HttpResponse(
            content=f"Unhandled Webhook received: {event['type']}", status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.suceeded webhook from stripe."""
        intent = event.data.object
        ic(intent)

        return HttpResponse(
            content=f"Webhook received: {event['type']} | SUCCESS : Created order in webhook",
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from stripe."""
        ic("handling a failed event")

        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200,
        )
