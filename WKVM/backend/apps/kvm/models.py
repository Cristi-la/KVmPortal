from django.db import models
from dataclasses import dataclass
from io import StringIO
import paramiko
from utils.models import BaseInfo


@dataclass
class AuthData:
    ip_fqdn: str
    username: str
    password: str = None
    port: int = 22
    pkey: str = None
    passphrase: str = None

    def __post_init__(self):
        if self.pkey:
            pkey_str = StringIO(self.pkey)
            self.pkey = paramiko.RSAKey.from_private_key(
                pkey_str, password=self.passphrase)

    def __str__(self):
        return f'AuthData({self.ip_fqdn}, {self.username})'


class Auth(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    pkey = models.CharField(max_length=16_384, null=True, blank=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    port = models.PositiveIntegerField(default=22)

    def __str__(self):
        return f'Auth({self.username})'

    def data(self):
        return self.from_data(
            username=self.username,
            password=self.password,
            port=self.port,
            pkey=self.pkey,
            passphrase=self.passphrase
        )

    @staticmethod
    def from_data(*args, **kwargs):
        return AuthData(*args, **kwargs)


class Tag(BaseInfo):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Base(BaseInfo):
    mgt_ip = models.GenericIPAddressField()
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True


class Hypervisor(Base):
    vms: models.QuerySet['VM']

    hostname = models.CharField(max_length=255)

    def __str__(self):
        return self.hostname


class VM(Base):
    name = models.CharField(max_length=255)
    hypervisor = models.ForeignKey(
        Hypervisor, on_delete=models.CASCADE, related_name='vms')

    def __str__(self):
        return self.name
