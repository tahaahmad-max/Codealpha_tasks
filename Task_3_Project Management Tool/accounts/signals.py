"""
Signals for the accounts app.
Automatically create a UserProfile when a new User is created.
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile automatically whenever a new user is registered."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Keep the profile saved when the user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
