from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import BaseTime

from apps.acc.managers import AccountManager

class Account(AbstractUser, BaseTime):
    objects = AccountManager()
    ...