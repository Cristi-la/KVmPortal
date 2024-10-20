# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from .models import UserProfile, Client

# @receiver(m2m_changed, sender=UserProfile.tenants.through)
# def manage_tenant_users(sender, instance, action, reverse, pk_set, **kwargs):
#     """
#     Signal to handle adding/removing a user from tenants when the tenants field is modified.
    
#     Arguments:
#     - instance: The UserProfile instance.
#     - action: The action being performed (pre_add, post_add, pre_remove, post_remove).
#     - reverse: A boolean indicating the direction of the relation.
#     - pk_set: The set of primary keys for the related objects being changed.
#     """

#     # Add users to tenants when they are selected
#     if action == "post_add":
#         tenants_added = Client.objects.filter(pk__in=pk_set)
#         for tenant in tenants_added:
#             tenant.add_user(instance)
#             print(f"User {instance.email} added to tenant {tenant.name}")

#     # Remove users from tenants when they are deselected
#     elif action == "post_remove":
#         tenants_removed = Client.objects.filter(pk__in=pk_set)
#         for tenant in tenants_removed:
#             # tenant.remove_user(instance)
#             print(f"User {instance.email} removed from tenant {tenant.name}")
