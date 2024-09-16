from django.db import models
from utils.models import BaseTime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from apps.common.models import Instance, UserInstanceManager
from django.contrib.auth.models import Group
from django.db.models import F, Case, When, Value, BooleanField

class Profile(BaseTime):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    is_readonly = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        unique_together = ('user', 'instance')

class Account(AbstractUser):
    profiles = models.ManyToManyField(Instance, blank=True, through='Profile')

    objects: UserInstanceManager = UserInstanceManager('profiles')

    @property
    def prof(self):
        current_instance = Instance.objects.get_current()

        return self.profiles.all().values(
            'id',
            'domain',
            'name',
            is_readonly=models.F('profile__is_readonly'),
            is_current=Case(
                When(profile__instance=current_instance, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

class AccountGroup(Group):
    class Meta:
        proxy = True
        app_label = 'acc'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'