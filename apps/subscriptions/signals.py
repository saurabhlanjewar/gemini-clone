from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.subscriptions.models import UserProfile
from apps.authentication.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
