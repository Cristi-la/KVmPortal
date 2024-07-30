from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
# from dataclasses import dataclass
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from apps.term.tasks import session_tasks
# from celery import chain
from channels.layers import get_channel_layer
from apps.term.models import Session
from utils.control.interface import Message
# import asyncio

# @dataclass
# class Message:
#     data: str = ''
#     type: str = ''
#     status: str = ''

#     def __dict__(self):
#         return {
#             'type': self.type.value,
#             'content': self.content,
#             'status': self.status.value
#         }

    # def addSessionBeat(self, data):
    #     tasks = PeriodicTask.objects.filter(name='every-10-seconds')

    #     if len(tasks)>0:
    #         print('Task get')
    #         task = tasks.first()
    #         # args = json.loads(task.args)
    #         # args = args[0]

    #         task.args = json.dumps(data)
    #         task.save()
    #     else:
    #         print('Task created')
    #         schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
    #         task = PeriodicTask.objects.create(interval = schedule, name='every-10-seconds', task='apps.term.tasks.update', args=json.dumps(data))


class TermConsumer(AsyncJsonWebsocketConsumer):
    users = set()
    channels = set()


    @database_sync_to_async
    def get_session(self) -> Session:
        session_id = self.scope['url_route']['kwargs']['session_id']

        try:
            # Check permissions
            session = Session.objects.get(pk=session_id)
            if not session.enable_console:
                session.consoleControl(enable=True)
            return session
        except Session.DoesNotExist:
            # close the connection
            ...
        
        return None
    

    async def connect(self):
        user = self.scope['user']
        self.session: Session = await self.get_session()
        print('Session:', self.session)

        if self.session is None:
            await super().close()
            return
        
        await self.channel_layer.group_add(
            self.session.downlink_session_id, 
            self.channel_name
        )
        
        await self.accept()
        self.users.add(user)
        self.channels.add(self.channel_name)

    async def disconnect(self, close_code):
        self.channels.remove(self.scope['user'])

        await self.session.async_consoleControl(enable=False)
        print('Disconet:', self.session)

        await self.channel_layer.group_discard(
            self.session.downlink_session_id, 
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        print('Receive:', content, f'SEND->{ self.session.downlink_session_id}')

        await self.channel_layer.group_send(
            self.session.downlink_session_id, {
                "type": "group.message", 
                "message": content
            }
        )

    async def group_message(self, event):
        message = event["message"]

        await self.send_json(
            content=message
        )


