# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from .models import Profile

@receiver(user_signed_up)
def create_profile(sender, request, user, **kwargs):
    # Create a profile instance for the newly registered user
    Profile.objects.create(user=user)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Save the profile whenever the associated user is saved
    instance.profile.save()
