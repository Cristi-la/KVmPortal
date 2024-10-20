from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from apps.term.models import Session
from utils.control.interface import Message
from django.conf import settings
import redis

r = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_CONTROLER_DB)

class TermConsumer(AsyncJsonWebsocketConsumer):
    user_sessions = set()

    def is_readonly(self, sid):
        for session in self.user_sessions:
            if session.pk == sid:
                return session.readonly 
            
        return False

    @database_sync_to_async
    def db_async(self, q, *args, **kwargs) -> Session:
        return q(self.user, *args, **kwargs)
    
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.accept()
            # print(f'Open socket for: {self.user}')
            return

        await self.close(code=4001)
        # print(f'Close socket for: {self.user}')

    async def disconnect(self, close_code):
        # print(f'Disconet user {self.user} from {self.user_sids}')

        for session in self.user_sessions:
            await self.channel_layer.group_discard(
                session.pk, self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        # print('Receive:', content)
        action = content.get('action')
        sid = content.get('sid')
        data = content.get('data')

        match action:
            case Message.SEND_DATA:
                print('Send data:', data, sid)
                if not self.is_readonly(sid):
                    r.publish(sid, data) 

            case Message.GET_SESSIONS:
                sids = await self.db_async(Session.manager.get_sessions)
                await self.send_json(Message.session(sids))

            case Message.GET_LOAD:
                await self.__handle_load(sid)

            case _:
                pass

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

    async def __handle_load(self, sid):
        session = await self.db_async(Session.manager.get_session_obj, sid)
        self.user_sessions.add(session)

        vis = session.get_visual_data()

        if not session.saveoutput:
            await self.send_json(Message.load(f"This session is configured to not save output\n", sid, vis))

        output = session.output # TODO

        await self.send_json(Message.load(output, sid, vis))
        await self.channel_layer.group_add(
            sid, self.channel_name
        )



