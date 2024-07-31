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

    @database_sync_to_async
    def get_user_sessions(self) -> Session:
        session = Session.objects.all().values_list('pk', flat=True)

        return list(session)
    
    @database_sync_to_async
    def get_session_output(self, sid) -> Session:
        self.user
        try:
            output = Session.objects.get(pk=sid).output
            return output
        except Session.DoesNotExist:
            return ''


    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.accept()
            print(f'Open socket for: {self.user}')
            return

        await self.close(code=4001)
        print(f'Close socket for: {self.user}')

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
        print('Receive:', content)
        action = content.get('action')
        sid = content.get('sid')
        data = content.get('data')


        match action:
            case Message.SEND_DATA:
                await self.send_group(sid, content=Message.data(data, sid))

            case Message.GET_SESSIONS:
                sids = await self.get_user_sessions()
                await self.send_json(Message.session(sids))

            case Message.GET_LOAD:
                output = await self.get_session_output(sid)
                await self.send_json(Message.load(output, sid))

                # Adding user to channel layer group
                await self.channel_layer.group_add(
                    sid, self.channel_name
                )

    async def send_group(self, sid, content):
        await self.channel_layer.group_send(
            sid, {
                "type": "group.message",
                "message": content
            }
        )

    async def group_message(self, event):
        message = event["message"]

        await self.send_json(
            content=message
        )
