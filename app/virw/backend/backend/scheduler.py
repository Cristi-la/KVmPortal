from tenant_schemas_celery.scheduler import TenantAwareScheduler
from django.utils import timezone

class ReadyTenantAwareScheduler(TenantAwareScheduler):
    # @classmethod
    # def get_queryset(cls):
    #     return super().get_queryset().filter(
    #         is_active=True,
    #         on_maintenance=False,
    #     )
    # ...
    ...