import paramiko
from dataclasses import dataclass
import asyncio


@dataclass
class Auth:
    username: str
    password: str
    key: str
    passphrase: str
    certificate: str


class AsyncSSHInterface:
    def __init__(self, ip_fqdn, auth):
        self.ip_fqdn = ip_fqdn
        self.auth = auth
        self.client = paramiko.SSHClient()

    async def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        await asyncio.get_event_loop().run_in_executor(None, self.client.connect, self.ip_fqdn, username=self.auth.username, password=self.auth.password)

    async def execute_command(self, command):
        stdin, stdout, stderr = await asyncio.get_event_loop().run_in_executor(None, self.client.exec_command, command)
        return stdout.read().decode()

    def close(self):
        self.client.close()
