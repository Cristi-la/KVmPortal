from django.db import models
from utils.models import BaseInfoMixin
from django.utils.translation import gettext_lazy as _
from django.db import connection
import os
import uuid
import os
import stat
from typing import Tuple, Optional
import urllib.parse
import hashlib

class KeyFile(BaseInfoMixin):
    
    def get_file_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('keys', filename)

    key_file = models.FileField(upload_to=get_file_path, max_length=255)
    passphrase = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"KeyFile({self.pk})"
    
    def set_permissions(self, permissions=stat.S_IREAD):
        try:
            os.chmod(self.key_file.path, permissions) 
        except PermissionError as e:
            ...
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.key_file and os.path.exists(self.key_file.path):
            self.set_permissions()

    def delete(self, *args, **kwargs):
        if self.key_file and os.path.exists(self.key_file.path):
            self.set_permissions(stat.S_IWRITE)
        super().delete(*args, **kwargs)

     
class Auth(BaseInfoMixin):
    class DriverType(models.TextChoices):
        QEMU = "qemu", _("QEMU")
        TEST = "test", _("TEST")

    class TransportType(models.TextChoices):
        # user, password, pkey, passphrase
        SSH = "ssh", _("ssh")
        # LIBSSH = "libssh", _("libssh")
        # LIBSSH2 = "libssh2", _("libssh2")
        # # -
        # UNIX = "unix", _("unix")
        # # extrac_params
        # EXT = "ext", _("ext")
        # # cert
        # TCP = "tcp", _("tcp")
        # TLS = "tls", _("tls")
        
    transport = models.CharField(max_length=50, choices=TransportType.choices, default=TransportType.SSH)
    driver = models.CharField(max_length=50, choices=DriverType.choices, default=DriverType.QEMU)
    port = models.PositiveIntegerField(default=22)
    path = models.CharField(max_length=255, null=True, blank=True, default='system')
    extrac_params = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='Extra parameters for the URI. Example: "key1=value1,key2=value2"'
    )

    username = models.CharField(max_length=255, default='anonymous')
    password = models.CharField(max_length=255, null=True, blank=True, help_text='Field displayed for preview only.')
    key_file = models.ForeignKey(KeyFile, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        method = 'password' if self.password else 'pkey'
        lead = 'Auth' if self.pk != 1 else 'DefaultAuth'

        return f'{lead}({self.username}, method={method}, port={self.port})'


class Tag(BaseInfoMixin):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    def has_view_permission(self, request, obj = ...):
        return True

    def __str__(self):
        return self.name
    

# --------------------------------------------------
# Mixins
# --------------------------------------------------

class HypervisorSSHMixin(models.Model):
    hostname = models.CharField(max_length=255)
    mgt_ip = models.GenericIPAddressField()
    auth = models.ForeignKey(Auth, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.hostname

    def internal_hostname(self):
        slug = connection.tenant.slug
        return f'host-{self.pk}-{slug}'
    
    def get_uri(self) -> str:
        ''' driver[+transport]://[username@][hostname][:port]/[path][?extraparameters] '''

        if self.auth is None:
            return None
        
        uri = self.auth.driver
        if self.auth.transport:
            uri += f"+{self.auth.transport}"

        uri += "://"
        if self.auth.username:
            uri += f"{self.auth.username}@"

        uri += self.internal_hostname()
        if self.auth.port and self.auth.port != 22:
            uri += f":{self.auth.port}"
        if self.auth.path:
            uri += f"/{self.auth.path}"
        if self.auth.extrac_params:
            encoded_params = urllib.parse.urlencode(dict(
                param.split('=') for param in self.auth.extrac_params.split(',')
            ))
            uri += f"?{encoded_params}"

        return uri

    # --------------------------------------------------
    # SSH config file
    # --------------------------------------------------
    def generate_ssh_config(self) -> str:
        if self.auth is None or self.auth.transport != Auth.TransportType.SSH:
            return

        config_lines = [
            f"Host {self.internal_hostname()}",
            f"    HostName {self.mgt_ip}",
            f"    User {self.auth.username}"
        ]

        if self.auth.port != 22:
            ssh_config += f"    Port {self.auth.port}\n"

        if self.auth.key_file and self.auth.key_file.key_file:
            config_lines.extend([
                f"    IdentityFile {self.auth.key_file.key_file.path}",
                "    IdentitiesOnly yes"
            ])
        elif self.auth.password:
            config_lines.extend([
                "    PasswordAuthentication yes",
                "    PubkeyAuthentication no"
            ])
        else:
            config_lines.extend([
                "    PasswordAuthentication no",
                "    PubkeyAuthentication yes"
            ])

        return "\n".join(config_lines)
    
    def _get_config_and_path(self, config_path: str) -> tuple[Optional[str], Optional[str]]:
        conf = self.generate_ssh_config()
        if not conf:
            return None, None

        # Expand user and make directory if needed
        path = os.path.expanduser(config_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return conf, path

    def _modify_config_file(self, path: str, action: str, conf: Optional[str] = None):
        # Read once, process in memory, then write once
        try:
            with open(path, "r", encoding="utf-8") as config_file:
                lines = config_file.readlines()
        except FileNotFoundError:
            lines = []

        new_config = []
        inside_target_host_block = False
        found_host = False
        hostname = self.internal_hostname()

        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("Host "):
                current_host = stripped_line.split(maxsplit=1)[1]
                inside_target_host_block = current_host == hostname
                if inside_target_host_block:
                    found_host = True
                    if action == 'update' and conf:
                        new_config.append(conf + "\n")
                    continue
            if not inside_target_host_block:
                new_config.append(line)
            elif line.strip() == "":
                inside_target_host_block = False

        if action == 'update' and not found_host and conf:
            new_config.append("\n" + conf + "\n")

        with open(path, "w", encoding="utf-8") as config_file:
            config_file.writelines(new_config)


    def append_config(self, config_path: str = "~/.ssh/config"):
        conf, path = self._get_config_and_path(config_path)
        if conf and path:
            with open(path, "a", encoding="utf-8") as config_file:
                config_file.write("\n" + conf + "\n")

    def update_config(self, config_path: str = "~/.ssh/config"):
        conf, path = self._get_config_and_path(config_path)
        if conf and path:
            self._modify_config_file(path, action='update', conf=conf)

    def remove_config(self, config_path: str = "~/.ssh/config"):
        path = os.path.expanduser(config_path)
        if os.path.exists(path):
            self._modify_config_file(path, action='remove')


class HashableTextFieldMixin(models.Model):
    """
    Mixin to add hash checking functionality to TextFields.
    """

    class Meta:
        abstract = True  # Ensure this mixin does not create its own table

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache original values of TextFields to avoid database queries
        self._original_textfield_values = {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if isinstance(field, models.TextField)
        }

    @staticmethod
    def compute_hash(content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to include hash checking.
        """
        updated_fields = kwargs.get('update_fields', None)
        fields_to_update = []

        # Check if the instance is being created or updated
        if self._state.adding:
            # For new instances, compute hashes for all TextFields
            for field in self._meta.fields:
                if isinstance(field, models.TextField):
                    field_name = field.name
                    hash_field_name = f"{field_name}_hash"
                    content = getattr(self, field_name)
                    if content:
                        new_hash = self.compute_hash(content)
                        setattr(self, hash_field_name, new_hash)
                        fields_to_update.append(hash_field_name)
        else:
            # For existing instances, compare current and original values
            for field_name, original_value in self._original_textfield_values.items():
                hash_field_name = f"{field_name}_hash"
                new_value = getattr(self, field_name)

                if new_value != original_value:
                    if new_value:
                        new_hash = self.compute_hash(new_value)
                        setattr(self, hash_field_name, new_hash)
                    else:
                        # If new content is None or empty, set hash to None
                        setattr(self, hash_field_name, None)
                    fields_to_update.append(hash_field_name)

        # Update 'update_fields' if provided
        if updated_fields is not None:
            updated_fields = set(updated_fields) | set(fields_to_update)
            kwargs['update_fields'] = list(updated_fields)

        super().save(*args, **kwargs)

        # After saving, update the cached original values
        for field_name in self._original_textfield_values.keys():
            self._original_textfield_values[field_name] = getattr(self, field_name)