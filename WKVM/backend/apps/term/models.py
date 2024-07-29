from typing import Any
from django.db import models
from apps.kvm.models import Hypervisor, VM
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from utils.models import BaseTime

# class Command(models.Model):
#     command = models.CharField(max_length=255,)
#     description = models.CharField(max_length=255, null=True, blank=True)
#     timeout = models.PositiveIntegerField(default=5, null=True, blank=True, help_text='Timeout in seconds')

#     def __str__(self):
#         return self.command
    
#     def insert_args(self, args):
#         return 
    

class Session(BaseTime):
    class Status(models.TextChoices):
        INIT = 'init', 'Init'
        RUNNING = 'running', 'Running'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    status = models.CharField(max_length=255, default=Status.INIT, choices=Status.choices)
    output = models.TextField(null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to = {"model__in": ('hypervisor', 'vm')}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Session({self.object_id}, {self.status})'
    
    @classmethod
    def init(cls, object_id, content_type):
        
        return cls.objects.create(
            status=cls.Status.INIT,

        )

    def get_uplink_session_id(self) -> str:
        return f's{self.pk}_up'

    def get_downlink_session_id(self) -> str:
        return f's{self.pk}_down'
    
    class Meta:
        index_together = [('content_type', 'object_id')]