
from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase, PermissionsMixinFacade
from tenant_users.tenants.models import UserProfile, UserProfileManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, connection
from django_tenants.utils import schema_context
from tenant_users.permissions.models import UserTenantPermissions

class Client(TenantBase):
    class ClientType(models.TextChoices):
        PRIVATE = "private", "Private"
        GLOBAL = "global", "Global"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, default=ClientType.GLOBAL.value, choices=ClientType.choices)
    
    enabled_until =  models.DateField(blank=True, null=True)
    is_trial = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    on_maintenance = models.BooleanField(default=False)

    def save(self, verbosity=1, *args, **kwargs):
        super().save(verbosity, *args, **kwargs)

        if self.owner is not None:
            with schema_context(self.schema_name):
                try:
                    obj = UserTenantPermissions.objects.get(profile=self.owner)
                    obj.is_staff = True
                    obj.is_superuser = True
                    obj.save()
                except UserTenantPermissions.DoesNotExist:
                    ...

    def __str__(self):
        if connection.schema_name == self.schema_name:
            return f'{self.name} (current)'
        return self.name
    
    

class ClientDomain(DomainMixin):
    pass

class TenantUserManager(UserProfileManager):
    def _create_user(self, *args, **kwargs):
        if kwargs.get('username') is None:
            raise ValueError("The given username must be set")
        
        return super()._create_user( *args, **kwargs)


class TenantUser(UserProfile):
    username_validator = UnicodeUsernameValidator()

    is_active = models.BooleanField("active", default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.")
    is_verified = models.BooleanField("verified", default=False, help_text="Designates whether this user has verified their email address.")


    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email',]

    objects = TenantUserManager()


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

