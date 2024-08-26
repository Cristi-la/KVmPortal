from django.db import models
from dataclasses import dataclass
from io import StringIO
import paramiko
from utils.models import BaseInfo
from django.core.exceptions import ValidationError

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
    username = models.CharField(max_length=255, default='anonymous')
    password = models.CharField(max_length=255, null=True, blank=True)
    pkey = models.CharField(max_length=16_384, null=True, blank=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    port = models.PositiveIntegerField(default=22)

    def __str__(self):
        method = 'password' if self.password else 'pkey'
        lead = 'Auth' if self.pk != 1 else 'DefaultAuth'

        return f'{lead}({self.username}, method={method}, port={self.port})'

class Tag(BaseInfo):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Base(BaseInfo):
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True

class Hypervisor(Base):
    vms: models.QuerySet['VM']

    hostname = models.CharField(max_length=255)

    # Only for development process
    mgt_ip = models.GenericIPAddressField()
    auth = models.ForeignKey(Auth, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname


class VM(Base):
    name = models.CharField(max_length=255)
    hypervisor = models.ForeignKey(
        Hypervisor, on_delete=models.CASCADE, related_name='vms')
    vcpu = models.PositiveIntegerField(blank=True, null=True)
    memory = models.PositiveIntegerField(blank=True, null=True)
    

    def __str__(self):
        return self.name
