from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseTime
from apps.common.managers import AccountManager
from django.conf import settings

class Profile(BaseTime):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Account(AbstractUser):
    profiles = models.ManyToManyField(Site, blank=True, through='Profile')

    objects = AccountManager()