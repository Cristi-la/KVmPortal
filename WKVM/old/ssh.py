from dataclasses import dataclass
import socket
import paramiko
import asyncio
from io import StringIO
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException


@dataclass
class Auth():
    ip_fqdn: str
    username: str
    password: str = None
    port: int = 22
    pkey: str = None
    passphrase: str = None

    def __init__(self, ip_fqdn, username, password=None, port=22, pkey=None, passphrase=None, **kwargs):
        self.ip_fqdn = ip_fqdn
        self.username = username
        self.port = port
        self.password = password
        self.pkey = pkey
        self.passphrase = passphrase

        if pkey:
            pkey_str = StringIO(self.key)
            self.pkey = paramiko.RSAKey.from_private_key(
                pkey_str, password=self.passphrase)


class SSHInterface():
    BUFFER_SIZE_LIMIT = 1024
    MIN_WIDTH = 80
    MIN_HEIGHT = 24

    def __init__(self,  term_type='xterm', auth=None, **kwargs):
        self.error = False
        self.close = False

        self.term_type = term_type
        self.auth = auth

        self.channel = None
        self.client = None

        self.pty_sizes = []

    def disconnect(self):
        if not self.is_active():
            return

        self.channel.close() # check later
        self.client.close()
        self.close = True

    async def __connect_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        loop = asyncio.get_running_loop()

        try:
            await loop.run_in_executor(None, lambda:
                ssh.connect(
                    hostname=self.auth.ip_fqdn,
                    port=self.auth.port,
                    username=self.auth.username,
                    password=self.auth.password,
                    pkey=self.auth.pkey,
                )          
            )
            
        except BadHostKeyException:
            raise Exception('Connection failed. Bad host key')
        except AuthenticationException:
            raise Exception('Connection failed. Authentication error')
        except SSHException:
            raise Exception('Connection failed. SSH error')
        except socket.error as e:
            raise Exception('Connection failed. Socket error', e)
        except Exception as e:
            raise Exception(f'Connection failed. {e}')
    
        return ssh

    async def __open_channel(self):
        loop = asyncio.get_running_loop()

        try:
            transport = await loop.run_in_executor(None, self.client.get_transport)
            channel = await loop.run_in_executor(None, transport.open_session)
            await loop.run_in_executor(None, lambda: channel.get_pty(term=self.term_type))
            await loop.run_in_executor(None, channel.invoke_shell)
            channel.setblocking(0)

            return channel

        except (paramiko.SSHException) as e:
            raise Exception('Connection failed. Could not open channel')
        except (socket.error, socket.timeout) as e:
            raise Exception('Connection failed. Socket error during channel opening', e)

    async def connect(self):
        self.client = await self.__connect_ssh()

        if self.client is None:
            raise Exception('Connection failed. Could not connect to SSH server')

        self.channel = await self.__open_channel()

        if self.channel is None:
            raise Exception('Connection failed. Could not open channel')
        

    async def send(self, data):
        if not self.is_active():
            return

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.channel.send, data)

    async def read(self):
        if not self.is_active():
            return

        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, self.channel.recv, 1024)
            decoded_data = data.decode('utf-8')
            return decoded_data
        except (paramiko.buffered_pipe.PipeTimeout, socket.timeout):
            pass

        if data is not None and data != '':
            updated_buffer = self.__get_buffer(self.id) + data
            self.__set_buffer(self.id, updated_buffer)

            if len(updated_buffer) >= self.BUFFER_SIZE_LIMIT:
                await self.__update_content(self.id)

        return data

    async def add_size(self, width, height):
        self.pty_sizes.append((width, height))
        self.resize_terminals()

    async def del_size(self, width, height):
        if (width, height) in self.pty_sizes:
            self.pty_sizes.remove((width, height))

    async def resize_terminals(self):
        if not self.is_active():
            return
        min_width = max(self.MIN_WIDTH, min(size[0] for size in self.pty_sizes))
        min_height = max(self.MIN_HEIGHT, min(size[1] for size in self.pty_sizes))

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            lambda: self.channel.resize_pty(width=min_width, height=min_height)
        )

    def is_active(self) -> bool:
        return not (self.error or self.close or self.client is None or self.channel is None)





if __name__ == '__main__':
    auth = Auth('localhost', 'Cristila', password='9907')
    sshint = SSHInterface(auth=auth)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sshint.connect())
    loop.run_until_complete(sshint.send('ipconfig'))
    
    import time
    time.sleep(2)

    loop.run_until_complete(sshint.read())

