from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

AuthUserModel = get_user_model()


@receiver(post_save, sender=AuthUserModel)
def create_profile(sender, instance, created, **kwargs):
    print("\nSignals post_save was caught!\n")
    if created:
        print("Created profile successfully")
        Profile(user=instance).save()
