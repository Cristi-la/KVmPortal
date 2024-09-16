# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Auth, Tag

@receiver(post_migrate, sender=Auth)
def create_default_auth(sender, **kwargs):
    if not Auth.objects.filter(pk=1).exists():
        Auth.objects.create(
            username='default',
            port=22,
        )

@receiver(post_migrate, sender=Tag)
def create_default_tags(sender, **kwargs):
    default_tags = [
        {"name": "KVM", "color": "#FF5733"},
        {"name": "Virtualization", "color": "#33FF57"},
        {"name": "Hypervisor", "color": "#3357FF"},
        {"name": "VM", "color": "#F39C12"},
        {"name": "QEMU", "color": "#8E44AD"},
        {"name": "Libvirt", "color": "#27AE60"},
        {"name": "Snapshot", "color": "#E74C3C"},
        {"name": "Live Migration", "color": "#1ABC9C"},
    ]

    for tag_data in default_tags:
        tag, created = Tag.objects.update_or_create(
            name=tag_data["name"],
            defaults={"color": tag_data["color"]},
        )