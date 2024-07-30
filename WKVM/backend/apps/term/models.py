from typing import Any
from django.db import models
from apps.kvm.models import Hypervisor, VM
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from utils.models import BaseTime
from channels.db import database_sync_to_async

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

    enable_console = models.BooleanField(default=False)
    save_output=models.BooleanField(default=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to = {"model__in": ('hypervisor', 'vm')}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Session({self.pk}, {self.object_id}, {self.status})'
    
    @classmethod
    def init(cls, object_id, content_type):
        content_type_instance = ContentType.objects.get(model=content_type)
        return cls.objects.create(
            status=cls.Status.INIT,
            object_id=object_id,
            content_type=content_type_instance
        )


    @property
    def uplink_session_id(self) -> str:
        return f's{self.pk}_up'

    @property
    def downlink_session_id(self) -> str:
        return f's{self.pk}_down'
    
    
    
    class Meta:
        index_together = [('content_type', 'object_id')]


    def consoleControl(self, enable=True):
        print('Console control changed to ', enable)
        if self.enable_console == enable:
            return
        
        self.enable_console = enable
        self.save()

    @database_sync_to_async
    def async_consoleControl(self, *args, **kwargs):
        self.consoleControl(*args, **kwargs)
