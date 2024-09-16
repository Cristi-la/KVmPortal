from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.acc.models import Account, Profile, AccountGroup
from django.contrib.auth.models import Group

admin.site.unregister(Group)  # Unregister from the default location

# Register under the Account app
@admin.register(AccountGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ['permissions']

class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1
    verbose_name_plural = 'Profiles'
    autocomplete_fields = ['instance']
    readonly_fields = ['created', 'updated']

class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


@admin.register(Account)
class AccountAdmin(UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    model = Account
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__instance')
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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'instance', 'updated', 'created')
    list_filter = ('instance',)
    search_fields = ('user__username', 'instance__domain')
    autocomplete_fields = ['user', 'instance']
    readonly_fields = ['created', 'updated']


