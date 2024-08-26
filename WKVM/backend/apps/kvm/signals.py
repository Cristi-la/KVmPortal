# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Auth

@receiver(post_migrate)
def create_default_auth(sender, **kwargs):
    if not Auth.objects.filter(pk=1).exists():
        Auth.objects.create(
            username='default',
            port=22,
        )