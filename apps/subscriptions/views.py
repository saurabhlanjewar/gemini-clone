import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Create customer if not already created
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.stripe_customer_id:
            customer = stripe.Customer.create(email=user.email)
            profile.stripe_customer_id = customer.id
            profile.save()
        else:
            customer = stripe.Customer.retrieve(profile.stripe_customer_id)

        checkout_session = stripe.checkout.Session.create(
            customer=customer.id,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_1RkKw0Iep6zADLtAtsXfmlLo",  # 👈 your actual Price ID here
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        return Response({"checkout_url": checkout_session.url})


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle subscription events
    if (
        event["type"] == "customer.subscription.created"
        or event["type"] == "customer.subscription.updated"
    ):
        stripe_customer_id = event["data"]["object"]["customer"]
        status = event["data"]["object"]["status"]

        profile = UserProfile.objects.get(stripe_customer_id=stripe_customer_id)
        if status == "active":
            profile.subscription_status = "pro"
        else:
            profile.subscription_status = "basic"
        profile.save()

    elif event["type"] == "customer.subscription.deleted":
        stripe_customer_id = event["data"]["object"]["customer"]
        profile = UserProfile.objects.get(stripe_customer_id=stripe_customer_id)
        profile.subscription_status = "basic"
        profile.save()

    return HttpResponse(status=200)


class SubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        return Response(
            {
                "subscription_status": profile.subscription_status,
                "daily_prompt_count": profile.daily_prompt_count,
            }
        )
