from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import sync_to_async
# from dataclasses import dataclass
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from apps.term.tasks import session_tasks
# from celery import chain
from channels.layers import get_channel_layer
from apps.term.models import Session
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
    @sync_to_async
    def get_session(self):
        try:
            # Check permissions
            return Session.objects.get(pk=self.session_id)
        except Session.DoesNotExist:
            # close the connection
            ...
        
        return None

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        
        session = await self.get_session()
        downlink_id = session.get_downlink_session_id()

        await self.channel_layer.group_add(
            downlink_id, 
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_id, 
            self.channel_name
        )

        # session_tasks.delay('192.168.8.103', 'kvm', 'kvm')

# async def send(self, data):
#         if not self.is_active():
#             return

#         loop = asyncio.get_running_loop()
#         await loop.run_in_executor(None, self.channel.send, data)

#     async def read(self):
#         if not self.is_active():
#             return

#         loop = asyncio.get_event_loop()
#         try:
#             data = await loop.run_in_executor(None, self.channel.recv, 1024)
#             decoded_data = data.decode('utf-8')
#             return decoded_data
#         except (paramiko.buffered_pipe.PipeTimeout, socket.timeout):
#             pass

        # session_tasks.delay('192.168.8.103', 'kvm', 'kvm')




        

    # @sync_to_async
    # def removeSessionBeat(self):
    #     task = PeriodicTask.objects.get(name='every-10-seconds')
    #     # args = json.loads(task.args)
    #     task.delete()
    #     task.args = json.dumps([])
    #     task.save()



    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name, {
    #             "type": "group_message", 
    #             "message": message
    #         }
    #     )


    # Receive message from room group
    async def group_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps(message)
        )