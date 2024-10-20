from django.contrib import admin
from apps.kvm.models import Tag
from django.db import connection
from utils.admin import BaseInfoAdmin
from django_tenants.utils import schema_context, tenant_context
from django_tenants.admin import TenantAdminMixin
from apps.private.forms import TenantUserAdminForm
from apps.common.models import TenantUser
from django.contrib.auth.admin import UserAdmin

from django_celery_beat.admin import (
    PeriodicTaskAdmin, CrontabScheduleAdmin, ClockedScheduleAdmin
)
from django_celery_results.admin import TaskResultAdmin
from django_celery_beat.models import (
    PeriodicTask, CrontabSchedule, IntervalSchedule, 
    SolarSchedule, ClockedSchedule
)
from django_celery_results.models import TaskResult
from django.contrib import admin


class TenantAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_header = "VIRW Admin"
        self.site_title = "VIRW Portal"
        self.index_title = "Welcome to the VIRW admin"


tenant_site = TenantAdminSite(name="tenant_admin")

# tenant_site.register(IntervalSchedule)
# tenant_site.register(SolarSchedule)
# tenant_site.register(PeriodicTask, PeriodicTaskAdmin)
# tenant_site.register(CrontabSchedule, CrontabScheduleAdmin)
# tenant_site.register(ClockedSchedule, ClockedScheduleAdmin)
tenant_site.register(TaskResult, TaskResultAdmin)

@admin.register(TenantUser, site=tenant_site)
class TenantUserAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", 'email', "password",)}),
        (
            "Account access",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                ),
            },
        ),
        (
            "Permissions (current tenant)",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Extra data",
            {
                "fields": ("last_login",),
                'classes': ('collapse',),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('username', "email", "password1", "password2"),
            },
        ),
        (
            "Account access",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )
    form = TenantUserAdminForm

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ("is_active", "is_verified")
    readonly_fields = ('last_login',)
    search_fields = ('username', 'email',)
    filter_horizontal = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(tenants=connection.tenant)

