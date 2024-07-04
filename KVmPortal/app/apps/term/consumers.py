import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class TermConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'main'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json['message'] if 'message' in text_data_json else ''

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.group_name, event)

        return await super().receive(text_data, bytes_data)

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))


