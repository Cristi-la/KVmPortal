from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from celery.result import AsyncResult
from apps.kvm.tasks import collect_data, ping_host

class TaskProgressConsumer(AsyncJsonWebsocketConsumer):
    group_names = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        for group_name in self.group_names:
            await self.channel_layer.group_discard(group_name, self.channel_name)
            print(f"User disconnect channel {self.group_name}")

    async def receive_json(self, content):
        if content.get('action') == 'start_task':
            task = await self.start_task()
            self.group_name = f'task_progress_{task.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            self.group_names.append(self.group_name)
            print(f"User join channel {self.group_name}")

    async def task_progress(self, event):
        progress = event['data']
        await self.send_json(progress)

    @sync_to_async
    def start_task(self,):
        return ping_host.delay(host='8.8.8.8')
        # return collect_data.delay(skip=False, hypervisor_id=1)

    
