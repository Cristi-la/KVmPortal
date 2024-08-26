from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, Profile
from django.contrib.sites.models import Site

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1
    verbose_name_plural = 'Profiles'
    autocomplete_fields = ['site']
    readonly_fields = ['created', 'updated']

class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    model = Account
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__site')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # Including the Profile inline in the Account admin view
    inlines = (ProfileInline,)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(Account, AccountAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'site')
    list_filter = ('site',)
    search_fields = ('user__username', 'site__domain')
    autocomplete_fields = ['user', 'site']

admin.site.register(Profile, ProfileAdmin)