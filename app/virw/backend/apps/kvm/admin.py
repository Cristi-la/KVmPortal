from django.contrib import admin
from apps.kvm.models import Tag
from apps.private.admin import tenant_site
from .models import (
    Hypervisor,
    Network,
    NetworkPort,
    HostInterface,
    NodeDevice,
    StoragePool,
    Domain,
    HostDevice,
    StorageVolume,
    NetworkInterface,
    NetworkFilter,
    Snapshot,
    DomainCheckpoint,
    KeyFile,
    Auth,
)
from utils.admin import BaseInfoAdmin, BaseTimeAdmin, BaseTabularInline


class ReadOnlyMixin(object):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# --------------------------------------------------------
# Auth classes
# --------------------------------------------------------
@admin.register(KeyFile, site=tenant_site)
class KeyFileAdmin(BaseInfoAdmin):
    list_display = ('id', 'path',)
    search_fields = ('id', 'key_file')
    
    def path(self, obj):
        return obj.key_file.path
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Auth, site=tenant_site)
class AuthAdmin(BaseInfoAdmin):
    list_display = ('id', 'username', 'driver', 'transport', 'port')
    search_fields = ('id', 'username', 'driver', 'transport', 'port')
    readonly_fields = ('password',)

    def has_change_permission(self, request, obj=None):
        return False
# --------------------------------------------------------
# Utility classes
# --------------------------------------------------------
@admin.register(Tag, site=tenant_site)
class TagAdmin(BaseInfoAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

# --------------------------------------------------------
# Inline classes
# --------------------------------------------------------

class TagInline(admin.TabularInline):
    model = Hypervisor.tags.through
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"
    

class VMTagInline(admin.TabularInline):
    model = Domain.tags.through
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

class NetworkInline(admin.TabularInline):
    model = Network
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StoragePoolInline(admin.TabularInline):
    model = StoragePool
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class NodeDeviceInline(admin.TabularInline):
    model = NodeDevice
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class HostInterfaceInline(admin.TabularInline):
    model = HostInterface
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class NetworkPortInline(admin.TabularInline):
    model = NetworkPort
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class StorageVolumeInline(admin.TabularInline):
    model = StorageVolume
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class HostDeviceInline(admin.TabularInline):
    model = HostDevice
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class NetworkInterfaceInline(admin.TabularInline):
    model = NetworkInterface
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class SnapshotInline(admin.TabularInline):
    model = Snapshot
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class DomainCheckpointInline(admin.TabularInline):
    model = DomainCheckpoint
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Hypervisor, site=tenant_site)
class HypervisorAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'mgt_ip', 'auth')
    search_fields = ('hostname', 'mgt_ip')
    inlines = [
        NetworkInline,
        StoragePoolInline,
        NodeDeviceInline,
        HostInterfaceInline,
        TagInline
    ]
    exclude = ('tags',)
    list_filter = ('auth',)

@admin.register(Network, site=tenant_site)
class NetworkAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'uuid', 'bridge_name', 'network_type')
    search_fields = ('name', 'uuid', 'bridge_name', 'network_type')
    list_filter = ('hypervisor', 'network_type')
    inlines = [NetworkPortInline]

@admin.register(NetworkPort, site=tenant_site)
class NetworkPortAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('port_number', 'network', 'status')
    search_fields = ('port_number', 'network__name', 'status')
    list_filter = ('network', 'status')

@admin.register(HostInterface, site=tenant_site)
class HostInterfaceAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'mac_address', 'interface_type')
    search_fields = ('name', 'mac_address', 'interface_type')
    list_filter = ('hypervisor', 'interface_type')

@admin.register(NodeDevice, site=tenant_site)
class NodeDeviceAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'device_type')
    search_fields = ('name', 'device_type')
    list_filter = ('hypervisor', 'device_type')

@admin.register(StoragePool, site=tenant_site)
class StoragePoolAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'uuid', 'pool_type', 'capacity', 'allocation', 'available')
    search_fields = ('name', 'uuid', 'pool_type')
    list_filter = ('hypervisor', 'pool_type')
    inlines = [StorageVolumeInline]

@admin.register(StorageVolume, site=tenant_site)
class StorageVolumeAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'storage_pool', 'domain', 'capacity', 'allocation', 'format_type')
    search_fields = ('name', 'path', 'format_type')
    list_filter = ('storage_pool', 'format_type', 'domain')

@admin.register(Domain, site=tenant_site)
class DomainAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'uuid', 'state', 'memory', 'vcpus')
    search_fields = ('name', 'uuid')
    list_filter = ('hypervisor', 'state')
    inlines = [
        HostDeviceInline,
        StorageVolumeInline,
        NetworkInterfaceInline,
        SnapshotInline,
        DomainCheckpointInline,
        VMTagInline,
    ]

@admin.register(HostDevice, site=tenant_site)
class HostDeviceAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('node_device', 'domain')
    search_fields = ('node_device__name', 'domain__name')
    list_filter = ('domain', 'node_device__hypervisor')

@admin.register(NetworkInterface, site=tenant_site)
class NetworkInterfaceAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('domain', 'mac_address', 'source_network', 'model_type', 'network_filter')
    search_fields = ('mac_address', 'model_type', 'domain__name')
    list_filter = ('source_network', 'model_type', 'domain')

@admin.register(NetworkFilter, site=tenant_site)
class NetworkFilterAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'hypervisor', 'uuid')
    search_fields = ('name', 'uuid')
    list_filter = ('hypervisor',)

@admin.register(Snapshot, site=tenant_site)
class SnapshotAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'domain', 'state')
    search_fields = ('name', 'domain__name')
    list_filter = ('domain', 'state')

@admin.register(DomainCheckpoint, site=tenant_site)
class DomainCheckpointAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'domain',)
    search_fields = ('name', 'domain__name')
    list_filter = ('domain',)