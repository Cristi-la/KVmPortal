import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from apps.term.control.interface import SSHInterface, Auth
from apps.term.control.host import Unix
import logging
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)
live_sessions = None

class TerminalStatus(Enum):
    Failing = 'Failing' 
    Work = 'Work'
    Init = 'Init'
    Undefined = 'Undefined'
    # Stopped = 'Stopped'
    # Abborted = 'Abborted'

class MessageType(Enum):
    Info = 'info'
    Error = 'error'
    Load = 'load_content'
    Unknow = 'unknow'

class UserAction(Enum):
    Execute = 'execute'
    Resize = 'resize'


@dataclass
class Message:
    content: str = ''
    type: MessageType = MessageType.Unknow
    status: TerminalStatus = TerminalStatus.Undefined

    def __dict__(self):
        return {
            'type': self.type.value,
            'content': self.content,
            'status': self.status.value
        }
    
    @classmethod
    def error(cls, e):
        return cls(
            content = str(e),
            type = MessageType.Error,
            status = TerminalStatus.Failing
        )




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
        auth = Auth('127.0.0.1', 'Cristila', '9907')
        session = SSHInterface(auth=auth)
        live_sessions = session

        return session

    @database_sync_to_async
    def __get_content(self):
        # This is a dummy content, replace with actual content
        return 'sdsdsd'

    async def connect(self, *args, **kwargs):
        sshint = await self.__get_session()

        await self.channel_layer.group_add(self.session_id, self.channel_name)
        await self.accept()

        await self.send_group_message(Message(
            type=MessageType.Load,
            status=TerminalStatus.Init,
            content=await self.__get_content(),
        ))

        try:
            await sshint.connect()
        except Exception as e:
            await self.send_group_message(
                Message.error('\n\r\n\r' + str(e))
            )
            return

        self.start_read()

    async def disconnect(self, code):
        sshint = await self.__get_session()

        if sshint is None or sshint.error or sshint.close:
            sshint.disconnect()

    async def send_group_message(self, message: Message, exclusive=False, myself=False):
        data = message.__dict__()

        print(f"Sending message: {data}")

        await self.channel_layer.group_send(
            self.session_id,
            {
                'type': 'group_message',
                'message': data,
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
        print(f"Received message: {message}")

        sshint = await self.__get_session()

        if sshint.is_active():
            await self.send_group_message(
                Message.error('Terminal is inactive. Connection failed. SSH error')
            )
            return

        action = message.get('action')
        data = message.get('data')
        logger.info(f"Received action: {action}")

        if action == UserAction.Execute.value and data:
            await sshint.send(data)
            self.start_read()

        elif action == UserAction.Resize.value:
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

            if sshint.is_active():
                await self.send_group_message(
                    Message.error('Connection failed. SSH error')
                )
                return

            data = await sshint.read()

            if data is not None:
                no_data_duration = 0
                await self.send_group_message(Message(
                        content=data,
                        type=MessageType.Info,
                        status=TerminalStatus.Work
                    )
                )
            else:
                no_data_duration += 0.1

            await asyncio.sleep(0.1)
