import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from apps.term.ssh.interfaces import SSHInterface, Auth
import logging

logger = logging.getLogger(__name__)
live_sessions = None


class TermConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = None
        self.read_task = None
        self.channel_name = None

        # this is a dummy session id, replace with actual session id
        self.session_id = '1'
        self.channel_name = 'test'

    @database_sync_to_async
    def __get_session(self) -> SSHInterface:
        global live_sessions

        if live_sessions:
            return live_sessions

        # This is a dummy auth object, replace with actual auth object
        auth = Auth('localhost', 22, 'root', 'password', None, None)
        session = SSHInterface(auth=auth)
        live_sessions = session

        print(f"Session created for {auth.ip_fqdn}")
        print(f"Session status: {session.error}, {session.close}")
        print(f"Session obj: {session.client}, {session.channel}")

        return session

    @database_sync_to_async
    def __get_content(self):
        # This is a dummy content, replace with actual content
        return 'sdsdsd'

    async def connect(self, *args, **kwargs):
        sshint = await self.__get_session()

        await self.channel_layer.group_add(self.session_id, self.channel_name)
        await self.accept()

        await self.send_group_message(
            msg_type='action',
            message={
                'type': 'load_content',
                'data': await self.__get_content()
            }
        )

        try:
            await sshint.connect()
        except Exception as e:
            await self.send_group_message(str(e))

        self.start_read()

        await self.send_group_message(
            msg_type='action',
            message={
                'type': 'load_content',
                'data': await self.__get_content()
            }
        )

        try:
            await sshint.connect()
        except Exception as e:
            await self.send_group_message(str(e))

        self.start_read()

    async def disconnect(self, code):
        sshint = await self.__get_session()

        if sshint is None or sshint.error or sshint.close:
            sshint.disconnect()

    async def send_group_message(self, message, exclusive=False, myself=False, msg_type=None):
        if msg_type is not None:
            message = {'type': msg_type, 'content': message}
        elif isinstance(message, Exception):
            message = {'type': 'error', 'content': str(message)}
        else:
            message = {'type': 'info', 'content': message}

        await self.channel_layer.group_send(
            self.session_id,
            {
                'type': 'group_message',
                'message': message,
                'to_myself': myself,
                'exclusive': exclusive,
                'sender_channel_name': self.channel_name
            }
        )

    async def group_message(self, event):
        if event.get('to_myself') is True and event.get('sender_channel_name') == self.channel_name and \
                event.get('sender_channel_name') is not None:
            await self.send(text_data=json.dumps({'message': event['message']}))
            return

        elif event.get('exclusive') is True:
            if event.get('sender_channel_name') != self.channel_name and event.get('sender_channel_name') is not None:
                await self.send(text_data=json.dumps({'message': event['message']}))
                return
            else:
                return

        await self.send(text_data=json.dumps({'message': event['message']}))

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        sshint = await self.__get_session()

        if sshint is None or sshint.error or sshint.close:
            return

        action = message.get('action')
        data = message.get('data')
        logger.info(f"Received action: {action}")

        if action == 'execute' and data:
            try:
                await sshint.send(data)
            except Exception as e:
                await self.send_group_message(str(e))
            self.start_read()

        elif action == 'resize':
            size = message.get('data')
            pty_size = (size.get('cols'), size.get('rows'))

            if message.get('type') == 'del':
                await sshint.del_size(*pty_size)

            elif message.get('type') == 'new':
                await sshint.add_size(*pty_size)

    def start_read(self):
        if self.read_task is None or self.read_task.done():
            self.read_task = asyncio.create_task(self.read())

    async def read(self):
        no_data_duration = 0

        while True:
            if no_data_duration >= 30:
                return

            sshint = await self.__get_session()

            if sshint is None or sshint.error or sshint.close:
                return

            data = await sshint.read()

            if data is not None:
                no_data_duration = 0
                await self.send_group_message(data)
            else:
                no_data_duration += 0.1

            await asyncio.sleep(0.1)
