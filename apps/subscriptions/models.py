from django.db import models
from apps.authentication.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    subscription_status = models.CharField(max_length=50, default="basic")  # basic, pro
    daily_prompt_count = models.IntegerField(default=0)
    last_prompt_date = models.DateField(null=True, blank=True)
