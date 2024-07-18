from apps.term.control.interface import SSHInterface, Auth
from apps.term.control.errors import InvalidSSHInterfaceError

local_auth = Auth('localhost', 'root')


class Unix():
    def __init__(self, sshint=None) -> None:
        if sshint is not None and isinstance(sshint, SSHInterface):
            raise InvalidSSHInterfaceError()
        self.sshint = sshint

    def execute_command(self):
        self.sshint.send('\n')

    def execute_script(self):
        pass

    def send_file(self):

        pass

    def __str__(self) -> str:
        if self.sshint and self.sshint.auth:
            return f'Remote({self.auth.ip_fgdn})'

        return 'Localhost()'


class Redhat(Unix):
    ...
