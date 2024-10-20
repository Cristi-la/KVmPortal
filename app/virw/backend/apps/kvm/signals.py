# signals.py
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from .models import Auth, KeyFile, Hypervisor
import os
import stat

# # --------------------------------------------------------
# #  Managing ssh config
# # --------------------------------------------------------
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
    

# # --------------------------------------------------------
# # KeyFile signals
# # --------------------------------------------------------
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
            os.chmod(old_file, stat.S_IWRITE)
            os.remove(old_file.path)