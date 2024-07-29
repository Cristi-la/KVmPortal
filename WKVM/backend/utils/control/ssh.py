
import paramiko
from threading import Thread
from apps.term.models import Auth

class SSHInterface():
    BUFFER_SIZE_LIMIT = 1024
    MIN_WIDTH = 80
    MIN_HEIGHT = 24
    MIN_TIMEOUT = 0

    def __init__(self,  auth:Auth.AuthData, term_type='xterm', width=80, height=24, **kwargs):
        self.term_type = term_type
        self.width = min(width, self.MIN_WIDTH)
        self.height = min(height, self.MIN_HEIGHT)
        self.auth = auth
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None
        self.timeout = min(kwargs.get('timeout'), self.MIN_TIMEOUT)

    def __connect(self):
        self.client.connect(
            hostname=self.auth.ip_fqdn,
            port=self.auth.port,
            username=self.auth.username,
            password=self.auth.password,
            pkey=self.auth.pkey,
            passphrase=self.auth.passphrase
        )

    def __perform(self, actions):
        for command in actions:
            self.shell.send(command + "\n")
        print("All actions completed.")

    def __read(self):
        try:
            while not self.shell.exit_status_ready():
                if self.shell.recv_ready():
                    output = self.shell.recv(1024).decode('utf-8')
                    self.reader_handler(output) 
        finally:
            print("Final output captured from the session.")

    def __start_threads(self, actions, reader_handler=None):
        self.reader_handler = reader_handler
        thread_executor = Thread(target=self.__perform, args=(actions, ))
        thread_reader = Thread(target=self.__read, args=())

        thread_executor.start()
        thread_reader.start()

        thread_executor.join()
        thread_reader.join()

    def run(self, actions, reader_handler=None):
        try:
            self.__connect()
            print("SSH connection established.")
            self.shell = self.client.invoke_shell(
                term=self.term_type,
                width=self.width,
                height=self.height,
            )
            # if self.timeout:
            #     self.shell.settimeout(self.timeout)
            print("Interactive SSH session started.")
            self.__start_threads(actions, reader_handler)
            

        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
        except paramiko.SSHException as e:
            print(f"SSH connection failed: {str(e)}")
        finally:
            self.client.close()
            print("SSH connection closed.")


        



