
import paramiko
from threading import Thread
from apps.kvm.models import Auth
import logging
import socket
from functools import wraps
from paramiko.ssh_exception import (
    AuthenticationException,
    BadAuthenticationType,
    BadHostKeyException,
    ChannelException,
    ConfigParseError,
    CouldNotCanonicalize,
    MessageOrderError,
    PasswordRequiredException,
    ProxyCommandFailure,
    SSHException,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_auth_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except PasswordRequiredException:
            self.buffer_sys_handler("Password is required for this operation.")
        except BadAuthenticationType as e:
            self.buffer_sys_handler(f"Bad authentication type encountered: {e.allowed_types}")
        except BadHostKeyException:
            self.buffer_sys_handler("The host key could not be verified.")
        except ChannelException as e:
            self.buffer_sys_handler(f"Problem with the SSH channel: {e.text}")
        except ConfigParseError:
            self.buffer_sys_handler("Error parsing SSH configuration.")
        except CouldNotCanonicalize:
            self.buffer_sys_handler("Unable to canonicalize address.")
        except AuthenticationException:
            self.buffer_sys_handler("Authentication failed - wrong credentials.")
        except MessageOrderError:
            self.buffer_sys_handler("Invalid order of SSH messages received.")
        except ProxyCommandFailure:
            self.buffer_sys_handler("Failure due to proxy command.")
        except SSHException as e:
            self.buffer_sys_handler(f"SSH error occurred: {e}")
        except socket.timeout:
            self.buffer_sys_handler("The connection timed out.")
        except socket.gaierror:
            self.buffer_sys_handler("Address-related error connecting to server.")
        except socket.error as e:
            self.buffer_sys_handler(f"Socket error occurred: {e}")
        except Exception as e:
            self.buffer_sys_handler(f"An unexpected error occurred: {e}")
        return None

    return wrapper


handle_shell_exceptions = handle_auth_exceptions

class SSHInterface:
    BUFFER_SIZE_LIMIT = 1024
    MIN_WIDTH = 80
    MIN_HEIGHT = 24
    MIN_TIMEOUT = 0
    TERM_TYPE = 'xterm'

    buffer = ""
    sys_buffer = ""

    def __init__(self, ip_fqdn, auth: Auth, **kwargs):
        self.ip_fqdn = ip_fqdn
        self.auth = auth
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

        self.height = self.MIN_HEIGHT
        self.width = self.MIN_WIDTH

    @handle_auth_exceptions
    def __connect(self):
        self.client.connect(
            hostname=self.ip_fqdn,
            port=self.auth.port,
            username=self.auth.username,
            password=self.auth.password,
            pkey=self.auth.pkey,
            passphrase=self.auth.passphrase
        )
        logger.info("SSH connection established.")

        return True

    @handle_shell_exceptions
    def __invoke_shell(self):
        self.shell = self.client.invoke_shell(
            term=self.TERM_TYPE,
            width=self.width,
            height=self.height,
        )
        logger.info("SSH connection established.")

        return True

    def __read(self):
        try:
            while not self.shell.exit_status_ready():
                if self.shell.recv_ready():
                    output = self.shell.recv(1024).decode('utf-8')
                    self.buffer_handler(output) 
        finally:
            logger.info("Final output captured from the session.")

    def __start_threads(self, actions):
        thread_executor = Thread(target=self.__perform, args=(actions, ))
        thread_reader = Thread(target=self.__read, args=())

        thread_executor.start()
        thread_reader.start()

        thread_executor.join()
        thread_reader.join()

    def __perform(self, actions):
        for command in actions:
            self.shell.send(command + "\n")
        print("All actions completed.")
    

    def run(self, actions):
        self.__connect()

        if not self.__connect():
            self.buffer_handler("Client not initialized.")
            return

        if not self.__invoke_shell():
            self.buffer_handler("Shell not initialized.")
            return
        
        logger.info("Interactive SSH session started.")
        self.__start_threads(actions)

    def buffer_handler(self, output):
        self.buffer += output
        
    def buffer_sys_handler(self, output):
        output = output + "\n"
        self.buffer_handler(output)
        self.sys_buffer += output

