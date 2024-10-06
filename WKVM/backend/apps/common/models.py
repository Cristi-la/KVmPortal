
from django.contrib.sites.models import Site, SiteManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.db.models import QuerySet
from django.conf import settings
from utils.models import BaseInfo

# class Instance(Site):


#     class InstanceType(models.TextChoices):
#         LOCAL = "LO", _("Local system")
#         REMOTE = "RE", _('Remote standalone system')

#         __empty__ = _("(Not selected)")

#     type = models.CharField(
#         max_length=2,
#         choices=InstanceType,
#         default=InstanceType.REMOTE,  # Optionally set a default value
#         help_text='Select the type of instance'
#     )


class Instance(Site):
    '''
    Define in Site model:
    @domain: models.CharField
    @name: models.CharField
    #objects: SiteManager
    '''

    def __str__(self):
        return self.name
    
    class Meta:
        proxy = True
        verbose_name = 'Instance'
        verbose_name_plural = 'instances'
        app_label = 'common'

class BaseInstanceManager(models.Manager):
    def __init__(self, field_name=None):
        super().__init__()
        self.__field_name = field_name
        self.__prefetch_related = [field_name] if field_name else []
        
    def on(self, instance: Instance) -> QuerySet:
        if isinstance(instance, Instance):
            return self.get_queryset().filter(**{self.__field_name: instance})
        raise ValueError(f"Expected 'Instance', got {type(instance).__name__}")
    
    def on_current(self) -> QuerySet:
        instance = Instance.objects.get_current()
        return self.get_queryset().filter(**{self.__field_name: instance})
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related(*self.__prefetch_related)
    

class UserInstanceManager(BaseInstanceManager, UserManager):
    pass



class BaseInstance(BaseInfo):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, default=settings.SITE_ID)

    objects = BaseInstanceManager('instance')

    class Meta:
        abstract = True


