from django.db import models
from utils.models import BaseTimeMixin
from django_tenants.admin import TenantAdminMixin
from dataclasses import dataclass
import hashlib
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import urllib.parse
import os
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid
import os
from typing import Tuple, Optional
import xml.etree.ElementTree as ET
from utils.control.parser import XMLParser
from utils.models import SeparatedCharField 
from django.db import transaction
from collections import defaultdict
from django.db import connection
import stat
from apps.kvm.simple_models import Tag, Auth, KeyFile
from apps.kvm.simple_models import HypervisorSSHMixin, HashableTextFieldMixin


# class XMLData(BaseInfoMixin):
#     class XMLType(models.TextChoices):

#         # Unique to Hypervisor
#         CAPABILITIES = "Capabilities", _("Domain capabilities")
#         SMBIOS = "SMBIOS", _('System Management BIOS (SMBIOS)')

#         # Unique to VM
#         DOMAIN = "Domain", _('Domain XML')

#         OTHER = "Other", _('Other XML data')

#     xml_type = models.CharField(max_length=50, choices=XMLType, default=XMLType.OTHER, null=False, blank=False)
#     xml_hash = models.CharField(max_length=256, blank=True, null=True, help_text="SHA-256 hash of the XML data. Leave blank to auto-calculate.")  # Field for storing SHA-256 hash
#     raw_xml = models.TextField()

#     def save(self, *args, **kwargs):
#         if not self.xml_hash or self._has_raw_xml_changed():
#             self.xml_hash = self.get_hash(self.raw_xml)

#         super().save(*args, **kwargs)

#     def _has_raw_xml_changed(self):
#         if not self.pk:
#             return True
#         orig = XMLData.objects.filter(pk=self.pk).values('raw_xml').first()
#         return orig and orig['raw_xml'] != self.raw_xml

#     @staticmethod
#     def clean_xml(raw_xml):
#         if raw_xml:
#             return raw_xml.strip().encode('utf-8')
#         return None

#     @staticmethod
#     def get_hash(data):
#         if data := XMLData.clean_xml(data):
#             return hashlib.sha256(data).hexdigest()
#         return None

#     def __str__(self):
#         return f"{self.xml_type}({self.xml_hash})"

# ########################################################
# #    Base objects for Hypervisor and VM
# #######################################################

# class Base(BaseTimeMixin):
#     tags = models.ManyToManyField(Tag, blank=True)
#     # xmls = models.ManyToManyField(XMLData, blank=True)

#     class Meta:
#         abstract = True

    # def save_xml(self, xml_type: XMLData.XMLType, raw_xml: str, ):
    #     if not raw_xml:
    #         return
        
    #     ref_xml_objs = self.xmls.filter(xml_type=xml_type).values('id','xml_hash').order_by('-created')

    #     if not ref_xml_objs.exists():
    #         self.xmls.create(xml_type=xml_type, raw_xml=raw_xml)
    #         return True
        
    #     ref_xml_hash = ref_xml_objs.first().get('xml_hash')
    #     curr_hash = XMLData.get_hash(raw_xml)

    #     if ref_xml_hash is None or ref_xml_hash != curr_hash:
    #         XMLData.objects.update(raw_xml=raw_xml, xml_hash=curr_hash)
    #         return True
        
    #     return False

    # def save_bulk_xml(self, data: list[tuple[XMLData.XMLType, str]]):
    #     if not data:
    #         return
        
    #     outputs = []
        
    #     for x in data:
    #         if len(x) != 2:
    #             continue
            
    #         xml_type, raw_xml = x
    #         if xml_type in XMLData.XMLType.values and raw_xml:
    #             outputs.append(self.save_xml(xml_type, raw_xml))

    #     to_parse = [d for d, output in zip(data, outputs) if output]
    #     self.parse_xmls(to_parse)

    #     if any(outputs):
    #         self.save()

    #     return outputs
    
    # def parse_xmls(self, data: list[tuple[XMLData.XMLType, str]]):
    #     raise NotImplementedError("Method parse_xmls must be implemented in child class.")

# class Hypervisor(Base):
#     vms: models.QuerySet['VM']

#     hostname = models.CharField(max_length=255)

#     # Only for development process
#     mgt_ip = models.GenericIPAddressField()
#     auth = models.ForeignKey(Auth, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    


    ### --------------------------------------------------
    ### XML parsing
    ### --------------------------------------------------
    # def save_xml(self, xml_type: XMLData.XMLType, raw_xml: str):
    #     if xml_type in [
    #         XMLData.XMLType.CAPABILITIES.value, 
    #         XMLData.XMLType.SMBIOS.value, 
    #         XMLData.XMLType.OTHER.value
    #     ]:
    #         return super().save_xml(xml_type, raw_xml)
    #     return False

    # # ----------------------------------------------
    # # Capabilities
    # # ----------------------------------------------
    # uuid = models.CharField(
    #     max_length=64, 
    #     blank=True, 
    #     null=True, 
    #     help_text="A unique identifier for the host system, which can be used to track the machine across reboots or virtual machine (VM) configurations."
    # )
    # arch = models.CharField(
    #     max_length=16, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The CPU architecture used by the host, which determines the instruction set architecture (ISA) available to virtual machines (VMs)."
    # )
    # model = models.CharField(
    #     max_length=64, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The specific CPU model, which can affect the feature set and performance characteristics available to VMs."
    # )
    # vendor = models.CharField(
    #     max_length=64, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The CPU vendor, such as 'Intel' or 'AMD'. This is crucial in determining the set of virtualization features supported by the processor."
    # )
    # microcode_version = models.CharField(
    #     max_length=16, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The microcode version of the CPU. Microcode updates provide patches at the CPU firmware level, including virtualization bug fixes and feature enhancements relevant to KVM."
    # )
    # signature_family = models.CharField(
    #     max_length=16, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The CPU signature family, which identifies the processor family and helps determine compatibility with certain KVM features or instructions."
    # )
    # signature_model = models.CharField(
    #     max_length=16, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The CPU signature model, identifying the specific CPU model within a family. This can affect the availability of certain virtualization instructions for KVM guests."
    # )
    # signature_stepping = models.CharField(
    #     max_length=16, 
    #     blank=True, 
    #     null=True, 
    #     help_text="The CPU stepping value, which indicates the revision of the processor. Certain virtualization features or improvements may only be available on specific steppings."
    # )
    # topology_sockets = models.IntegerField(
    #     blank=True, 
    #     null=True, 
    #     help_text="The number of physical CPU sockets. In KVM, this is useful for assigning specific sockets to virtual machines to improve CPU topology awareness in the guest."
    # )
    # topology_dies = models.IntegerField(
    #     blank=True, 
    #     null=True, 
    #     help_text="The number of dies per socket. A die is a single continuous piece of silicon that contains the CPU cores. This helps configure virtual CPU topology in KVM."
    # )
    # topology_clusters = models.IntegerField(
    #     blank=True, 
    #     null=True, 
    #     help_text="The number of clusters per die. Clusters help group CPU cores, and understanding this helps configure advanced CPU topology for KVM guests."
    # )
    # topology_cores = models.IntegerField(
    #     blank=True, 
    #     null=True, 
    #     help_text="The number of CPU cores available per socket. This helps determine how many virtual CPUs (vCPUs) can be allocated to KVM guests and the configuration of those vCPUs."
    # )
    # topology_threads = models.IntegerField(
    #     blank=True,
    #     null=True, 
    #     help_text="The number of threads per core, which indicates the hyper-threading capability of the CPU. Virtual machines can take advantage of this to increase the number of vCPUs per core."
    # )
    # features = SeparatedCharField(
    #     help_text="A list of CPU features supported by the host, such as 'vmx:smx:rdrand'. These features can be passed through to KVM guests."
    # )
    # pages = SeparatedCharField(
    #     help_text="Supported memory page sizes (in KiB), such as 4KiB or 2MiB. KVM can use these page sizes to map guest memory more efficiently, affecting memory performance in virtual machines."
    # )

    # suspend_mem = models.BooleanField(
    #     default=False,
    #     help_text="Indicates if suspend to memory (S3) is supported, which allows VMs to save their state to memory and resume execution later."
    # )
    # suspend_disk = models.BooleanField(
    #     default=False,
    #     help_text="Indicates if suspend to disk (S4) is supported, which allows VMs to save their state to disk and resume execution later, even after a power off."
    # )
    # suspend_hybrid = models.BooleanField(
    #     default=False,
    #     help_text="Indicates if hybrid suspend is supported, combining suspend to memory (S3) and suspend to disk (S4) to allow faster resume while protecting against power loss."
    # )

    # iommu_support = models.BooleanField(
    #     default=False,
    #     help_text="Indicates if IOMMU (Input/Output Memory Management Unit) support is enabled. This is essential for device passthrough to VMs, allowing them direct access to hardware."
    # )

    # live_migration = models.BooleanField(
    #     default=False,
    #     help_text="Indicates if live migration is supported, allowing VMs to be moved between hosts without downtime."
    # )
    # uri_transports = SeparatedCharField(
    #     help_text="A list of supported URI transport protocols for migration. This defines the network protocols used for live migration of VMs."
    # )

    # cache_banks = models.JSONField(
    #     blank=True,
    #     null=True,
    #     help_text="A list of cache banks for each CPU level. Each entry contains the cache level, type, size, and associated CPUs."
    # )

    # secmodels = models.JSONField(
    #     blank=True,
    #     null=True,
    #     help_text="A list of security models supported by the host, such as 'selinux' or 'apparmor'."
    # )
    # # ----------------------------------------------
    # # SMBIOS
    # # ----------------------------------------------

    # def __parse_capabilities(self, raw_xml: str):
    #     x = XMLParser(raw_xml)
    #     self.uuid = x.val(".//host/uuid")
    #     self.arch = x.val(".//host/cpu/arch")
    #     self.model = x.val(".//host/cpu/model")
    #     self.vendor = x.val(".//host/cpu/vendor")
    #     self.microcode_version = x.attr(".//host/cpu/microcode", "version")
    #     self.signature_family = x.attr(".//host/cpu/signature", "family")
    #     self.signature_model = x.attr(".//host/cpu/signature", "model")
    #     self.signature_stepping = x.attr(".//host/cpu/signature", "stepping")
    #     self.topology_sockets = x.attr(".//host/cpu/topology", "sockets", data_type=int)
    #     self.topology_dies = x.attr(".//host/cpu/topology", "dies", data_type=int)
    #     self.topology_clusters = x.attr(".//host/cpu/topology", "clusters", data_type=int)
    #     self.topology_cores = x.attr(".//host/cpu/topology", "cores", data_type=int)
    #     self.topology_threads = x.attr(".//host/cpu/topology", "threads", data_type=int)
    #     self.features = x.list_of_attr(".//cpu/feature", "name")
    #     self.pages = x.list_of_attr(".//cpu/pages", "size", data_type=int)
    #     self.suspend_mem = x.val(".//host/power_management/suspend_mem") is not None
    #     self.suspend_disk = x.val(".//host/power_management/suspend_disk") is not None
    #     self.suspend_hybrid = x.val(".//host/power_management/suspend_hybrid") is not None
    #     self.iommu_support = x.attr(".//host/iommu", "support", default="no") == "yes"
    #     self.live_migration = x.val('.//host/migration_features/live') is not None
    #     self.uri_transports = x.list_of_val('.//host/migration_features/uri_transports/uri_transport')
    #     self.cache_banks = x.list_of_dict('.//host/cache/bank', {
    #         'level': (None, int),
    #         'type': (None, str),
    #         'size': (None, int),
    #         'unit': (None, str),
    #         'cpus': (None, str),
    #     })
    #     self.secmodels = x.list_of_dict('.//host/secmodel', {
    #         "model": str,
    #         "doi": (0, int),
    #     })


    # def __parse_smbios(self, raw_xml: str):
    #     ...

    # def __parse_other(self, raw_xml: str):
    #     ...
    
    # def parse_xmls(self, data: list[tuple[XMLData.XMLType, str]]):
    #     for xml_type, raw_xml in data:
    #         match xml_type:
    #             case XMLData.XMLType.CAPABILITIES:
    #                 self.__parse_capabilities(raw_xml)
    #             case XMLData.XMLType.SMBIOS:
    #                 self.__parse_smbios(raw_xml)
    #             case XMLData.XMLType.OTHER:
    #                 self.__parse_other(raw_xml)
    #             case _:
    #                 ...


# class VM(Base):
#     interfaces: models.QuerySet['VMInterface']

#     class State(models.TextChoices):
#         RUNNING = 'running', _('Running')
#         IDLE = 'idle', _('Idle')
#         PAUSED = 'paused', _('Paused')
#         IN_SHUTDOWN = 'in shutdown', _('In Shutdown')
#         SHUT_OFF = 'shut off', _('Shut Off')
#         CRASHED = 'crashed', _('Crashed')
#         PMSUSPENDED = 'pm suspended', _('PM Suspended')

#         TRANSITION = 'transition', _('Transition')
#         NO_INFO = 'no info', _('No Info')

#     hypervisor = models.ForeignKey(
#         Hypervisor, on_delete=models.CASCADE, related_name='vms')
#     state = models.CharField(max_length=50, choices=State.choices, default=State.NO_INFO)

#     def __str__(self):
#         if self.name:
#             return self.name
#         return '-'
    
#     ### --------------------------------------------------
#     ### XML parsing
#     ### --------------------------------------------------
#     # def save_xml(self, xml_type: XMLData.XMLType, raw_xml: str):
#     #     if xml_type in [
#     #         XMLData.XMLType.DOMAIN.value,
#     #     ]:
#     #         return super().save_xml(xml_type, raw_xml)
#     #     return False
#     # # ----------------------------------------------
#     # # Domain
#     # # ----------------------------------------------
#     # name = models.CharField(
#     #     max_length=255,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The name of the virtual machine."
#     # )
#     # domain_type = models.CharField(
#     #     max_length=16,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The type of the domain (e.g., 'kvm')."
#     # )
#     # uuid = models.CharField(
#     #     max_length=64, 
#     #     blank=True, 
#     #     null=True, 
#     #     help_text="The UUID of the virtual machine."
#     # )

#     # memory = models.BigIntegerField(
#     #     blank=True,
#     #     null=True,
#     #     help_text="The amount of memory allocated to the virtual machine in kilobytes."
#     # )
#     # current_memory = models.BigIntegerField(
#     #     blank=True,
#     #     null=True,
#     #     help_text="The current memory allocation of the virtual machine."
#     # )
#     # dump_core = models.BooleanField(
#     #     default=False,
#     #     help_text="Indicates if core dumps are enabled for the virtual machine."
#     # )

#     # vcpu = models.IntegerField(
#     #     blank=True,
#     #     null=True,
#     #     help_text="The number of virtual CPUs allocated to the virtual machine."
#     # )
#     # vcpu_placement = models.CharField(
#     #     max_length=16,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The CPU placement strategy (e.g., 'static', 'dynamic')."
#     # )
#     # os_type = models.CharField(
#     #     max_length=64,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The type of the operating system (e.g., 'hvm')."
#     # )
#     # os_arch = models.CharField(
#     #     max_length=16,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The architecture of the operating system"
#     # )
#     # os_machine = models.CharField(
#     #     max_length=64,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The machine type of the operating system"
#     # )
#     # boot_device = models.CharField(
#     #     max_length=16,
#     #     blank=True,
#     #     null=True,
#     #     help_text="The boot device used by the virtual machine"
#     # )

#     # features = SeparatedCharField(
#     #     help_text="The features enabled for the virtual machine."
#     # )

#     # cpu_mode = models.CharField(max_length=64, blank=True, null=True, help_text="CPU mode (e.g., 'host-passthrough').")
#     # cpu_check = models.CharField(max_length=64, blank=True, null=True, help_text="CPU check setting.")
#     # cpu_migratable = models.BooleanField(default=False, help_text="Whether the CPU is migratable.")
    
#     # clock_offset = models.CharField(max_length=16, blank=True, null=True, help_text="Clock offset (e.g., 'utc').")
#     # clock_timezone = models.CharField(max_length=64, blank=True, null=True, help_text="Clock timezone.")
#     # clock_adjustment = models.CharField(max_length=256, blank=True, null=True, help_text="Clock adjustment policy.")
#     # timers = models.JSONField(blank=True, null=True, help_text="Timers configuration.")

#     # on_poweroff = models.CharField(max_length=16, blank=True, null=True, help_text="Action on power off.")
#     # on_reboot = models.CharField(max_length=16, blank=True, null=True, help_text="Action on reboot.")
#     # on_crash = models.CharField(max_length=16, blank=True, null=True, help_text="Action on crash.")
    
#     # pm_suspend_to_mem = models.BooleanField(default=False, help_text="Whether suspend to memory is enabled.")
#     # pm_suspend_to_disk = models.BooleanField(default=False, help_text="Whether suspend to disk is enabled.")

#     # emulator = models.CharField(max_length=255, blank=True, null=True, help_text="The emulator used by the virtual machine.")

#     # def __parse_domain(self, raw_xml: str):
#     #     x = XMLParser(raw_xml)
#     #     self.domain_type = x.attr("./", "type")
#     #     self.uuid = x.val(".//uuid", default="")
#     #     self.name = x.val(".//name", default=self.uuid)
#     #     self.memory = x.val(".//memory", data_type=int)
#     #     self.current_memory = x.val(".//currentMemory", data_type=int)
#     #     self.dump_core = x.val(".//memory", "dumpCore") == "on"
#     #     self.vcpu = x.val(".//vcpu", data_type=int)
#     #     self.vcpu_placement = x.attr(".//vcpu", "placement")
#     #     self.os_type = x.val(".//os/type")
#     #     self.os_arch = x.attr(".//os/type", "arch")
#     #     self.os_machine = x.attr(".//os/type", "machine")
#     #     self.boot_device = x.attr(".//os/boot", "dev")
#     #     self.features = x.list_of_name(".//features")
#     #     self.cpu_mode = x.attr(".//cpu", "mode")
#     #     self.cpu_check = x.attr(".//cpu", "check")
#     #     self.cpu_migratable = x.val(".//cpu", "migratable") == "on"

#     #     self.clock_offset = x.attr(".//clock", "offset")
#     #     self.clock_timezone = x.attr(".//clock", "timezone")
#     #     self.clock_adjustment = x.attr(".//clock", "adjustment")
#     #     self.timers = x.list_of_dict(".//clock/timer", {
#     #         "name": str,
#     #         "tickpolicy": str,
#     #         "present": str,
#     #     })

#     #     self.on_poweroff = x.val(".//on_poweroff")
#     #     self.on_reboot = x.val(".//on_reboot")
#     #     self.on_crash = x.val(".//on_crash")
#     #     self.pm_suspend_to_mem = x.attr(".//pm/suspend-to-mem", "enabled") == "yes"
#     #     self.pm_suspend_to_disk = x.attr(".//pm/suspend-to-disk", "enabled") == "yes"
#     #     self.emulator = x.val(".//devices/emulator")

#     #     interfaces = x.extract_as_list(".//devices/interface")
#     #     self.__parse_vm_interfaces(interfaces)

#     # def __parse_vm_interfaces(self, raw_xml: str):
#     #     interfaces_to_update = []
#     #     interfaces_to_create = []

#     #     existing_interfaces = defaultdict(list)
#     #     for interface in self.interfaces.all():
#     #         existing_interfaces[interface.mac].append(interface)

#     #     for interface_xml in raw_xml:
#     #         x = XMLParser(interface_xml)
#     #         mac_address = x.attr(".//mac", "address")

#     #         if mac_address and mac_address in existing_interfaces:
#     #             vm_interface = existing_interfaces[mac_address].pop(0)
#     #         else:
#     #             vm_interface = VMInterface(vm=self)

#     #         vm_interface.parse_interface(interface_xml)

#     #         if vm_interface.pk:
#     #             interfaces_to_update.append(vm_interface)
#     #         else:
#     #             interfaces_to_create.append(vm_interface)

#     #     interfaces_to_delete = [iface for iface_list in existing_interfaces.values() for iface in iface_list]

#     #     with transaction.atomic():
#     #         if interfaces_to_update:
#     #             VMInterface.objects.bulk_update(
#     #                 interfaces_to_update,
#     #                 fields=['mac', 'static_mac', 'source_type', 'source_network', 'source_dev', 'source_bridge',
#     #                         'target_dev', 'target_managed', 'model_type', 'if_type', 'apci_index']
#     #             )
#     #         if interfaces_to_create:
#     #             VMInterface.objects.bulk_create(interfaces_to_create)

#     #         if interfaces_to_delete:
#     #             VMInterface.objects.filter(id__in=[iface.id for iface in interfaces_to_delete]).delete()

#     # def parse_xmls(self, data: list[tuple[XMLData.XMLType, str]]):
#     #     for xml_type, raw_xml in data:
#     #         match xml_type:
#     #             case XMLData.XMLType.DOMAIN:
#     #                 self.__parse_domain(raw_xml)
#     #             case _:
#     #                 ...


# class VMInterface(BaseInfoMixin):
#     vm = models.ForeignKey(VM, on_delete=models.CASCADE, related_name='interfaces')

#     mac = models.CharField(max_length=17, null=True, blank=True)
#     static_mac = models.BooleanField(default=False)

#     source_type = models.CharField(max_length=255, null=True, blank=True)
#     source_network = models.CharField(max_length=255, null=True, blank=True)
#     source_dev = models.CharField(max_length=255, null=True, blank=True)
#     source_bridge = models.CharField(max_length=255, null=True, blank=True)

#     target_dev = models.CharField(max_length=255, null=True, blank=True)
#     target_managed = models.BooleanField(default=False)

#     model_type = models.CharField(max_length=255, null=True, blank=True)
#     if_type = models.CharField(max_length=255, null=True, blank=True)
#     apci_index = models.IntegerField(null=True, blank=True)

#     def parse_interface(self, raw_xml: str):
#         x = XMLParser(raw_xml)
        
#         self.if_type = x.attr(".//interface", "type")
#         self.mac = x.attr(".//mac", "address")
#         self.static_mac = x.attr(".//mac", "static", default="yes") == "yes"

#         self.source_network = x.attr(".//source", "network")
#         self.source_dev = x.attr(".//source", "dev")
#         self.source_bridge = x.attr(".//source", "bridge")
#         self.source_type = x.attr(".//source", "type")
        
#         self.target_dev = x.attr(".//target", "dev")
#         self.model_type = x.attr(".//model", "type")
#         self.apci_index = x.attr(".//acpi", "index", data_type=int)

#     def __str__(self):
#         if self.source_type:
#             return f'{self.source_type}({self.mac})'
#         return '-'
    

class Base(BaseTimeMixin):

    class Meta:
        abstract = True




# --------------------------------------------------
#   Hypervisor
# --------------------------------------------------
class Hypervisor(HashableTextFieldMixin, HypervisorSSHMixin, Base):
    tags = models.ManyToManyField(Tag, blank=True)
    """
    Represents a hypervisor host machine.
    """
    # hostname: models.CharField
    # mgt_ip: models.GenericIPAddressField
    # auth: models.ForeignKey[Auth, None, None]

    capabilities_xml = models.TextField(null=True, blank=True)
    capabilities_xml_hash = models.CharField(max_length=64, null=True, blank=True)  # SHA-256 hash

    sysinfo_xml = models.TextField(null=True, blank=True)
    sysinfo_xml_hash = models.CharField(max_length=64, null=True, blank=True)  # SHA-256 hash

    def __str__(self):
        return self.hostname

class Network(Base):
    """
    Represents a virtual network managed by the hypervisor.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='networks')
    
    name = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=36, null=True, blank=True)
    bridge_name = models.CharField(max_length=255, null=True, blank=True)
    network_type = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.name} ({self.hypervisor.hostname})"

class NetworkPort(Base):
    """
    Represents a network port associated with a virtual network.
    """
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='ports')
    port_number = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"Port {self.port_number} on {self.network.name}"

class HostInterface(Base):
    """
    Represents physical or virtual host interfaces.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='host_interfaces')
    name = models.CharField(max_length=255, null=True, blank=True)
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    interface_type = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.name} ({self.hypervisor.hostname})"

class NodeDevice(Base):
    """
    Represents physical hardware devices on the host.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='node_devices')
    name = models.CharField(max_length=255, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.name} ({self.hypervisor.hostname})"

class StoragePool(Base):
    """
    Represents a storage pool on the hypervisor.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='storage_pools')
    name = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=36, null=True, blank=True)
    pool_type = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.BigIntegerField(null=True, blank=True)
    allocation = models.BigIntegerField(null=True, blank=True)
    available = models.BigIntegerField(null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.name} ({self.hypervisor.hostname})"

# --------------------------------------------------
#   VM
# --------------------------------------------------

class Domain(Base):
    tags = models.ManyToManyField(Tag, blank=True)
    mgt_ip = models.GenericIPAddressField(null=True, blank=True)
    """
    Represents a virtual machine domain.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='domains')
    name = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=36, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    memory = models.BigIntegerField(help_text="Memory size in KiB", null=True, blank=True)
    vcpus = models.IntegerField(null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return self.name

class HostDevice(Base):
    """
    Represents a host device assigned to a domain (e.g., GPU passthrough).
    """
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='host_devices')
    node_device = models.ForeignKey(NodeDevice, on_delete=models.CASCADE, related_name='assigned_to_domains')
    # Additional fields as needed

    def __str__(self):
        return f"{self.node_device.name} assigned to {self.domain.name}"

class StorageVolume(Base):
    """
    Represents a storage volume used by a domain.
    """
    storage_pool = models.ForeignKey(StoragePool, on_delete=models.CASCADE, related_name='volumes')
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, related_name='storage_volumes', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=512, null=True, blank=True)
    capacity = models.BigIntegerField(null=True, blank=True)
    allocation = models.BigIntegerField(null=True, blank=True)
    format_type = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.name} ({self.storage_pool.name})"

class NetworkInterface(Base):
    """
    Represents a network interface attached to a domain.
    """
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='network_interfaces')
    source_network = models.ForeignKey(Network, on_delete=models.SET_NULL, null=True, related_name='network_interfaces')
    network_filter = models.ForeignKey('NetworkFilter', on_delete=models.SET_NULL, null=True, blank=True, related_name='network_interfaces')
    
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    model_type = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.domain.name} - {self.mac_address}"

class NetworkFilter(Base):
    """
    Represents a network filter applied to a domain's network interface.
    """
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, related_name='network_filters')
    name = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=36, null=True, blank=True)
    # xml = models.TextField(help_text="XML definition of the network filter", null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return self.name

class Snapshot(Base):
    """
    Represents a snapshot of a domain.
    """
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='snapshots')
    name = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    # Additional fields as needed

    def __str__(self):
        return f"{self.domain.name} - Snapshot {self.name}"

class DomainCheckpoint(Base):
    """
    Represents a checkpoint of a domain.
    """
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='checkpoints')
    name = models.CharField(max_length=255, null=True, blank=True)
    # xml = models.TextField()
    # Additional fields as needed

    def __str__(self):
        return f"{self.domain.name} - Checkpoint {self.name})"