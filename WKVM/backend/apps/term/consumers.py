from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from apps.term.models import Session
from utils.control.interface import Message


class TermConsumer(AsyncJsonWebsocketConsumer):
    # users = set()
    # channels = set()

    # @database_sync_to_async
    # def get_session(self) -> Session:
    #     # session_id = self.scope['url_route']['kwargs']['session_id']
    #     session_id = 1

    #     try:
    #         # Check permissions
    #         session = Session.objects.get(pk=session_id)
    #         if not session.enable_console:
    #             session.consoleControl(enable=True)
    #         return session
    #     except Session.DoesNotExist:
    #         # close the connection
    #         ...

    #     return None

    async def connect(self):
        user = self.scope['user']

        # if user.is_authenticated:
        await self.accept()
        # print(f'Open socket for {user}')
        return

        await self.close(code=4001)
        print(f'Close socket for {user}')

        # self.session: Session = await self.get_session()
        # print('Session:', self.session)

        # if self.session is None:
        #     await super().close()
        #     return

        # await self.channel_layer.group_add(
        #     self.session.downlink_session_id,
        #     self.channel_name
        # )
        # self.users.add(user)
        # self.channels.add(self.channel_name)

    async def disconnect(self, close_code):
        ...
        # self.channels.remove(self.scope['user'])

        # await self.session.async_consoleControl(enable=False)
        # print('Disconet:', self.session)

        # await self.channel_layer.group_discard(
        #     self.session.downlink_session_id,
        #     self.channel_name
        # )

    async def receive_json(self, content, **kwargs):
        # action = content.action
        print('Receive:', content,
              f'SEND->{ self.session.downlink_session_id}')

        # match action:
        #     case Message.SESSIONS:
        #         send()

        #     await send()

    async def send(self, sid, content):
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
