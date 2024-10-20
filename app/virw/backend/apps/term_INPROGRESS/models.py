from typing import Any
from django.db import models
from apps.kvm.models import Hypervisor, VM
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from utils.models import BaseTime
from django.db.models import Manager
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist

def handleDoseNotExist(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ObjectDoesNotExist:
            return None

    return wrapper

class SessionManager(models.QuerySet):
    def permission(self, user):
        return self.filter(attach=True) # TODO
    
    @handleDoseNotExist
    def get_session_obj(self, user, sid):
        return self.permission(user).get(pk=sid)
    
    def get_sessions(self, user):
        sids = self.permission(user).values_list('pk', flat=True)
        return list(sids)
    
    @handleDoseNotExist
    def get_session_fields(self, user, sid, *fields):
        session = self.permission(user).get(pk=sid)
        return {
            field: getattr(session, field, None) for field in fields
        }
    

class Session(BaseTime):
    get_downlink = lambda pk: f's{pk}_down'

    class Status(models.TextChoices):
        INIT = 'init', 'Init'
        RUNNING = 'running', 'Running'

        CLOSED = 'closed', 'Closed'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    status = models.CharField(
        max_length=255, default=Status.INIT, choices=Status.choices)
    output = models.TextField(null=True, blank=True)

    attach = models.BooleanField(default=False)
    readonly = models.BooleanField(default=True)
    saveoutput = models.BooleanField(default=True) # TODO

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to={"model__in": ('hypervisor', 'vm')}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    manager = SessionManager.as_manager()
    objects = Manager()

    def __str__(self):
        return f'Session({self.pk}, {self.object_id}, {self.status})'

    @classmethod
    def init(cls, object_id, content_type, status=Status.INIT):
        content_type_instance = ContentType.objects.get(model=content_type)
        return cls.objects.create(
            status=status,
            object_id=object_id,
            content_type=content_type_instance
        )


    def get_visual_data(self):
        return {
            # 'name': str(self.content_object),
            # 'name': 'rightd',
            'readonly': self.readonly,
            # 'created': self.content_object.created,
        }

    class Meta:
        index_together = [('content_type', 'object_id')]
