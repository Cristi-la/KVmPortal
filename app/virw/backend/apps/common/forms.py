# forms.py

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import TenantUser, Client
from django.core.exceptions import ValidationError
from apps.private.forms import TenantUserAdminForm


class UserAdminForm(TenantUserAdminForm):
    tenants = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        required=False,
        label='',
        widget=FilteredSelectMultiple('Tenants', is_stacked=False)
    )

    def clean(self):
        cleaned_data = super().clean()
        tenants_to_remove = set(self.initial.get('tenants', [])) - set(cleaned_data.get('tenants', []))

        for tenant in tenants_to_remove:
            if tenant.owner.pk == self.instance.pk:
                raise ValidationError({'tenants':f"You cannot remove the current tenant owner from: {'tenant'}"})
                    
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance
        
        if user.pk:
            self.fields['tenants'].initial = user.tenants.all()
        else:
            self.fields['tenants'].initial = []

    def save(self, commit=True):
        tenants: list[Client] = self.cleaned_data.pop('tenants', [])

        user: TenantUser = super().save(commit=commit)

        if tenants is not None:
            current_tenants: set[Client] = set(user.tenants.all())

            new_tenants: set[Client] = set(tenants)
            tenants_to_add = new_tenants - current_tenants
            tenants_to_remove = current_tenants - new_tenants

            for tenant in tenants_to_add:
                tenant.add_user(user)

            for tenant in tenants_to_remove:
                tenant.remove_user(user)

        return user