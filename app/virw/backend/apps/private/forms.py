# forms.py

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from apps.common.models import TenantUser
from django.db import connection
from django.core.exceptions import ValidationError
from tenant_users.permissions.models import UserTenantPermissions
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField
)


class TenantUserAdminForm(UserChangeForm):

    is_superuser = forms.BooleanField(
        label="Superuser status",
        help_text=(
            "Designates that this user has all permissions without "
            "explicitly assigning them"
        ),
        required=False,
    )
    is_staff = forms.BooleanField(
        label="Staff status",
        help_text=(
            "Designates whether the user can log into this admin site"
        ),
        required=False,
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='',
        widget=FilteredSelectMultiple('groups', is_stacked=False)
    )

    @staticmethod
    def get_limit_choices():
        if connection.schema_name == 'public':
            return {'content_type__app_label__in': ['common', 'auth', 'admin', 'permissions']}

        return Q(content_type__app_label__in=['admin', 'auth', 'kvm', 'permissions']) | \
            Q(content_type__app_label='common', content_type__model='tenantuser')


    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label='',
        limit_choices_to=get_limit_choices,
        widget=FilteredSelectMultiple('user permissions', is_stacked=False)
    )

    class Meta:
        model = TenantUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            tenant_perms = self.instance.tenant_perms
            self.fields['groups'].initial = tenant_perms.groups.all()
            self.fields['user_permissions'].initial = tenant_perms.user_permissions.all()
            self.fields['is_superuser'].initial = tenant_perms.is_superuser
            self.fields['is_staff'].initial = tenant_perms.is_staff
        except UserTenantPermissions.DoesNotExist:
            self.fields['groups'].initial = []
            self.fields['user_permissions'].initial = []
            self.fields['is_superuser'].initial = False
            self.fields['is_staff'].initial = False

    def clean(self):
        cleaned_data = super().clean()

        tenant = connection.tenant

        if tenant.owner.pk == self.instance.pk:
            if not cleaned_data.get('is_superuser', False):
                raise ValidationError({'is_superuser': f"You cannot remove this flag from the tenant owner of: {tenant}"})
            if not cleaned_data.get('is_staff', False):
                raise ValidationError({'is_staff': f"You cannot remove this flag from the tenant owner of: {tenant}"})

        return cleaned_data


    def save(self, commit=True):
        is_superuser: bool = self.cleaned_data.pop('is_superuser', False)
        is_staff: bool = self.cleaned_data.pop('is_staff', False)
        groups: list[Group] = self.cleaned_data.pop('groups', [])
        user_permissions: list[Permission] = self.cleaned_data.pop('user_permissions', [])

        user: TenantUser = super().save(commit=False)
        if commit:
            user.save()

        try:
            tenant_perms: UserTenantPermissions = user.tenant_perms
            tenant_perms.is_superuser = is_superuser
            tenant_perms.is_staff = is_staff
            tenant_perms.groups.set(groups)
            tenant_perms.user_permissions.set(user_permissions)
            tenant_perms.save()
        except UserTenantPermissions.DoesNotExist:
            ...
        
        return user

