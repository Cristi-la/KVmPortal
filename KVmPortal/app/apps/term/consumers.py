import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class TermConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json['message'] if 'message' in text_data_json else ''

        # Code to start/interact with SSH session to remote hosts
        # ...

        response = {
            'type': 'send_message',
            'message': 'SSH session started',
        }

        await self.send(text_data=json.dumps(response))

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
