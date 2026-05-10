from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import UserProfile, Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        Cart.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()