from django.contrib import admin
from apps.common.models import Instance
from django.contrib.sites.models import Site
from django.conf import settings

# Unregister the default Site admin
admin.site.unregister(Site)

@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')
    search_fields = ('id', 'domain', 'name')
    ordering = ('domain',)

    def has_change_permission(self, request, obj=None):
        if obj and obj.id == settings.SITE_ID:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.id == settings.SITE_ID:
            return False
        return super().has_delete_permission(request, obj)