from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from apps.common.models import Client, ClientDomain, TenantUser
from django.contrib import admin
from .models import TenantUser, Client
from django.contrib import admin
from apps.common.models import TenantUser
from django.db import connection
from apps.private.admin import TenantUserAdmin
from apps.common.forms import UserAdminForm

class DomainInline(admin.TabularInline):
    model = ClientDomain
    extra = 1

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'slug', 'enabled_until', 'is_trial', 'is_active', 'on_maintenance', 'created', 'modified')
    search_fields = ('name', 'schema_name', 'slug')
    fieldsets = (
        (None, {'fields': ('name', 'schema_name', 'owner', 'type' )}),
        ('Additional', {'fields': ('slug', 'description' )}),
        ('Management', {'fields': ('enabled_until', 'is_trial', 'is_active', 'on_maintenance', )}),
        ('Info', {'fields': ('created', 'modified', ), 'classes': ('collapse',)},),
    )
    inlines = [DomainInline]
    list_filter = ('is_trial', 'is_active', 'on_maintenance')
    readonly_fields = ('created', 'modified', 'domain_url')
    ordering = ('name',)
    

@admin.register(ClientDomain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain',)
    list_filter = ('is_primary',)
    ordering = ('domain',)



@admin.register(TenantUser)
class UserAdmin(TenantUserAdmin):

    form = UserAdminForm

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ("is_active", "is_verified")
    readonly_fields = ('last_login',)
    search_fields = ('username', 'email',)
    ordering = ("username", )
    filter_horizontal = []

    tenants_fieldset = (
        "Tenants",
        {
            "fields": ("tenants",),
        },
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets_list = list(super().get_fieldsets(request, obj))
        fieldsets_list.insert(-1, self.tenants_fieldset)
        fieldsets = tuple(fieldsets_list)

        if obj is None:
            return [ fieldset for fieldset in fieldsets if fieldset[0] != "Permissions (current tenant)"]

        if connection.tenant in obj.tenants.all():
            return fieldsets

        return [fieldset for fieldset in fieldsets if fieldset[0] != "Permissions (current tenant)"]


    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
    

