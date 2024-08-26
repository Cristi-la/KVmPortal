from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sites.models import Site
from .models import Account, Profile

@receiver(post_save, sender=Account)
def create_default_profile(sender, instance, created, **kwargs):
    if created:
        default_site = Site.objects.get(id=settings.SITE_ID)
        Profile.objects.get_or_create(user=instance, site=default_site)
