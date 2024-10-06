# signals.py
from django.db.models.signals import post_migrate, post_delete, pre_save, post_save
from django.dispatch import receiver
from .models import Auth, Tag, KeyFile, Hypervisor
import os

# --------------------------------------------------------
# Creating default objects
# --------------------------------------------------------
@receiver(post_migrate, sender=Auth)
def create_default_auth(sender, **kwargs):
    if not Auth.objects.filter(pk=1).exists():
        Auth.objects.create(
            username='admin',
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

# --------------------------------------------------------
#  Managing ssh config
# --------------------------------------------------------
@receiver(post_save, sender=Hypervisor)
def create_ssh_config(sender, instance: Hypervisor, created, **kwargs):
    if instance.auth is None:
        instance.remove_config()
        return
        
    if instance.auth.transport != Auth.TransportType.SSH:
        return
    
    if created:
        instance.append_config()
        return
    
    instance.update_config()
    

# --------------------------------------------------------
# KeyFile signals
# --------------------------------------------------------
@receiver(post_delete, sender=KeyFile)
def auto_delete_file_on_delete(sender, instance: KeyFile, **kwargs):
    """
    Deletes file from filesystem
    when corresponding  object is deleted.
    """
    if instance.key_file:
        if os.path.isfile(instance.key_file.path):
            os.remove(instance.key_file.path)

@receiver(pre_save, sender=KeyFile)
def auto_delete_file_on_change(sender, instance: KeyFile, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = KeyFile.objects.get(pk=instance.pk).key_file
    except KeyFile.DoesNotExist:
        return False

    new_file = instance.key_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)