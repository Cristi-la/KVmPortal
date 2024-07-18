class InvalidSSHInterfaceError(Exception):
    """Exception raised for invalid SSHInterface."""

    def __init__(self, message="SSHint must be an instance of SSHInterface"):
        self.message = message
        super().__init__(self.message)
