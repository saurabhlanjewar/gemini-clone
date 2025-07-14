from django.urls import path
from .views import CreateSubscriptionView, stripe_webhook, SubscriptionStatusView

urlpatterns = [
    path("subscribe/pro", CreateSubscriptionView.as_view()),
    path("webhook/stripe", stripe_webhook),
    path("subscription/status", SubscriptionStatusView.as_view()),
]
