from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.acc.models import Account, Profile
from apps.common.models import Instance


@receiver(post_save, sender=Account)
def create_default_profile(sender, instance, created, **kwargs):
    if created:
        default_instance = Instance.objects.get_current()
        Profile.objects.get_or_create(user=instance, instance=default_instance)

