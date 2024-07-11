from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Account(AbstractUser):
    pass


class Instance(Site):
    '''
    Define in Site model:
    @domain: models.CharField
    @name: models.CharField
    #objects: SiteManager
    '''

    class InstanceType(models.TextChoices):
        LOCAL = "LO", _("Local system")
        REMOTE = "RE", _('Remote standalone system')

        __empty__ = _("(Not selected)")

    type = models.CharField(
        max_length=2,
        choices=InstanceType,
        default=InstanceType.REMOTE,  # Optionally set a default value
        help_text='Select the type of instance'
    )

    def clean(self):
        super().clean()

        errors = {}

        if errors:
            raise ValidationError(errors)



