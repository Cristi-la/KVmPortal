from django.db import models
from dataclasses import dataclass
import hashlib
from apps.common.models import BaseInstance, BaseInstanceManager
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# @dataclass
# class AuthData:
#     ip_fqdn: str
#     username: str
#     password: str = None
#     port: int = 22
#     pkey: str = None
#     passphrase: str = None

#     def __post_init__(self):
#         if self.pkey:
#             pkey_str = StringIO(self.pkey)
#             self.pkey = paramiko.RSAKey.from_private_key(
#                 pkey_str, password=self.passphrase)

#     def __str__(self):
#         return f'AuthData({self.ip_fqdn}, {self.username})'


# # 

class Auth(BaseInstance):
    class DriverType(models.TextChoices):
        QEMU = "qemu", _("QEMU")
        TEST = "test", _("TEST")

    class TransportType(models.TextChoices):
        # user, password, pkey, passphrase
        SSH = "ssh", _("ssh")
        LIBSSH = "libssh", _("libssh")
        LIBSSH2 = "libssh2", _("libssh2")

        # -
        UNIX = "unix", _("unix")

        # extrac_params
        EXT = "ext", _("ext")

        # cert
        TCP = "tcp", _("tcp")
        TLS = "tls", _("tls")
        
    transport = models.CharField(max_length=50, choices=TransportType, default=TransportType.SSH)
    driver = models.CharField(max_length=50, choices=DriverType, default=DriverType.QEMU)                            
    port = models.PositiveIntegerField(default=22)
    path = models.CharField(max_length=255, null=True, blank=True)
    extrac_params = models.CharField(max_length=255, null=True, blank=True)
    
    username = models.CharField(max_length=255, default='anonymous')
    password = models.CharField(max_length=255, null=True, blank=True)
    pkey = models.CharField(max_length=16_384, null=True, blank=True)
    passphrase = models.CharField(max_length=255, null=True, blank=True)

    def get_uri(self, host: str = 'localhost') -> str:
        # driver[+transport]://[username@][hostname][:port]/[path][?extraparameters]

        uri = self.driver
        if self.transport and self.transport != self.TransportType.SSH:
            uri += f"+{self.transport}"

        uri += "://"
        if self.username:
            uri += f"{self.username}@"

        uri += host
        if self.port and self.port != 22:
            uri += f":{self.port}"
        if self.path:
            uri += f"/{self.path}"
        if self.extrac_params:
            uri += f"?{self.extrac_params}"

        return uri
    
    objects: BaseInstanceManager

    def __str__(self):
        method = 'password' if self.password else 'pkey'
        lead = 'Auth' if self.pk != 1 else 'DefaultAuth'

        return f'{lead}({self.username}, method={method}, port={self.port})'

class Tag(BaseInstance):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    objects: BaseInstanceManager

    def __str__(self):
        return self.name

########################################################
#    ########    # Base objects for Hypervisor and VM
########################################################
class XMLData(BaseInstance):
    class XMLType(models.TextChoices):
        CAPABILITIES = "CAPABILITIES", _("Domain capabilities")
        SMBIOS = "SMBIOS", _('System Management BIOS (SMBIOS)')
        OTHER = "OTHER", _('Other XML data')

        __empty__ = _("(Not selected)")

    xml_type = models.CharField(max_length=50, choices=XMLType, default=XMLType.OTHER)
    xml_hash = models.CharField(max_length=256, blank=True, null=True)  # Field for storing SHA-256 hash
    raw_xml = models.TextField()

    def save(self, *args, **kwargs):
        if self.xml_hash is None:
            self.xml_hash = XMLData.get_hash(self.raw_xml)

        super().save(*args, **kwargs)

    @staticmethod
    def clean_xml(raw_xml):
        if raw_xml:
            return raw_xml.strip().encode('utf-8')
        return None

    @staticmethod
    def get_hash(data):
        if data := XMLData.clean_xml(data):
            return hashlib.sha256(data).hexdigest()
        return None

    def __str__(self):
        return f"{self.xml_type}({self.xml_hash})"


class Base(BaseInstance):
    tags = models.ManyToManyField(Tag, blank=True)
    xmls = models.ManyToManyField(XMLData, blank=True)
    objects: BaseInstanceManager

    class Meta:
        abstract = True

    def process_common_xml(self, xml_type: XMLData.XMLType, raw_xml: str, ):
        if not raw_xml:
            return
        
        ref_xml_objs = self.xmls.filter(xml_type=xml_type).values('id','xml_hash').order_by('-created')

        if not ref_xml_objs.exists():
            self.xmls.create(xml_type=xml_type, raw_xml=raw_xml)
            return True
        
        ref_xml_hash = ref_xml_objs.first().get('xml_hash')
        curr_hash = XMLData.get_hash(raw_xml)

        if ref_xml_hash is None or ref_xml_hash != curr_hash:
            XMLData.objects.update(raw_xml=raw_xml, xml_hash=curr_hash)
            return True
        
        return False

    def proccess_bulk_xml(self, data):
        if not data:
            return
        
        outputs = []
        
        for x in data:
            if len(x) != 2:
                continue
            
            xml_type, raw_xml = x
            if xml_type in XMLData.XMLType.values and raw_xml:
                outputs.append(self.process_common_xml(xml_type, raw_xml))

        return outputs

class Hypervisor(Base):
    vms: models.QuerySet['VM']

    hostname = models.CharField(max_length=255)

    # Only for development process
    mgt_ip = models.GenericIPAddressField()
    auth = models.ForeignKey(Auth, default=1, on_delete=models.CASCADE)

    # Basic host information
    uuid = models.CharField(max_length=36, blank=True, null=True)
    
    # CPU details
    cpu_arch = models.CharField(max_length=20, blank=True, null=True)
    cpu_model = models.CharField(max_length=100, blank=True, null=True)
    cpu_vendor = models.CharField(max_length=50, blank=True, null=True)
    cpu_microcode_version = models.CharField(max_length=10, blank=True, null=True)
    
    # Signature
    cpu_signature_family = models.CharField(max_length=10, blank=True, null=True)
    cpu_signature_model = models.CharField(max_length=10, blank=True, null=True)
    cpu_signature_stepping = models.CharField(max_length=10, blank=True, null=True)
    
    # CPU Topology and features
    cpu_topology_sockets = models.IntegerField(blank=True, null=True)
    cpu_topology_dies = models.IntegerField(blank=True, null=True)
    cpu_topology_clusters = models.IntegerField(blank=True, null=True)
    cpu_topology_cores = models.IntegerField(blank=True, null=True)
    cpu_topology_threads = models.IntegerField(blank=True, null=True)
    
    # List of CPU features
    cpu_features = ArrayField(models.CharField(max_length=50), default=list)
    
    # Memory pages
    memory_pages = ArrayField(models.CharField(max_length=50), default=list)
    
    # Power management features
    power_management = ArrayField(models.CharField(max_length=50), default=list)
    
    # IOMMU support
    iommu_support = models.BooleanField(default=False)
    
    # Migration features
    migration_live = models.BooleanField(default=False)
    uri_transports = ArrayField(models.CharField(max_length=50), default=list)
    
    # Topology of NUMA cells
    # cells_memory = ArrayField(models.CharField(max_length=50), default=list)
    # cells_pages = ArrayField(models.CharField(max_length=50), default=list)
    
    # Distances and CPU information inside each NUMA cell
    # cells_distances = ArrayField(models.CharField(max_length=50), default=list)
    # cells_cpus = ArrayField(models.CharField(max_length=50), default=list)
    
    # Cache information
    # cache_banks = ArrayField(models.CharField(max_length=50), default=list)
    
    # Security models
    secmodel_model = models.CharField(max_length=50, blank=True, null=True)
    secmodel_doi = models.CharField(max_length=10, blank=True, null=True)
    # secmodel_baselabels = ArrayField(models.CharField(max_length=255), default=list)
    

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
