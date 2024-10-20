from rest_framework import serializers
from .models import (
    Domain,
    HostDevice,
    StorageVolume,
    NetworkInterface,
    NetworkFilter,
    Snapshot,
    DomainCheckpoint,
    Tag, 
    Hypervisor,
    NodeDevice,
    StoragePool,
    Network,
)
from rest_flex_fields import FlexFieldsModelSerializer


class BaseSerializer(FlexFieldsModelSerializer):
    ...

class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag 
        fields = '__all__'

class HostDeviceSerializer(BaseSerializer):
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())
    node_device = serializers.PrimaryKeyRelatedField(queryset=NodeDevice.objects.all())

    class Meta:
        model = HostDevice
        fields = '__all__'

class StorageVolumeSerializer(BaseSerializer):
    storage_pool = serializers.PrimaryKeyRelatedField(queryset=StoragePool.objects.all())
    domain = serializers.PrimaryKeyRelatedField(
        queryset=Domain.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = StorageVolume
        fields = '__all__'

class NetworkInterfaceSerializer(BaseSerializer):
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())
    source_network = serializers.PrimaryKeyRelatedField(
        queryset=Network.objects.all(), allow_null=True, required=False
    )
    network_filter = serializers.PrimaryKeyRelatedField(
        queryset=NetworkFilter.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = NetworkInterface
        fields = '__all__'


class NetworkFilterSerializer(BaseSerializer):
    hypervisor = serializers.PrimaryKeyRelatedField(queryset=Hypervisor.objects.all())

    class Meta:
        model = NetworkFilter
        fields = '__all__'


class SnapshotSerializer(BaseSerializer):
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())

    class Meta:
        model = Snapshot
        fields = '__all__'

class DomainCheckpointSerializer(BaseSerializer):
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())

    class Meta:
        model = DomainCheckpoint
        fields = '__all__'

class HypervisorSerializer(BaseSerializer):
    class Meta:
        model = Hypervisor
        fields = '__all__'

class NodeDeviceSerializer(BaseSerializer):
    hypervisor = serializers.PrimaryKeyRelatedField(queryset=Hypervisor.objects.all())

    class Meta:
        model = NodeDevice
        fields = '__all__'

class StoragePoolSerializer(BaseSerializer):
    hypervisor = serializers.PrimaryKeyRelatedField(queryset=Hypervisor.objects.all())

    class Meta:
        model = StoragePool
        fields = '__all__'


class HypervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hypervisor
        fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    hypervisor = HypervisorSerializer(read_only=True)
    hypervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=Hypervisor.objects.all(), source='hypervisor', write_only=True
    )
    class Meta:
        model = Domain
        fields = '__all__'











# # Meta serializers
# class VMAbstractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VM
#         fields = ['id','name', 'vcpu', 'memory', 'state', 'created', 'updated']

# class HypervisorAbstractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hypervisor
#         fields = ['id', 'hostname', 'mgt_ip']

# class TagAbstractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', 'description', 'color']

# class XmlAbstractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = XMLData
#         fields = ['id', 'xml_type']



# # Acuall serializers
# class TagSerializer(BaseSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'


# class HypervisorSerializer(BaseSerializer):
#     tags = TagAbstractSerializer(many=True, read_only=True)
#     vms = VMAbstractSerializer(many=True, read_only=True)
#     xmls = XmlAbstractSerializer(many=True, read_only=True)

#     class Meta:
#         model = Hypervisor
#         fields = '__all__'

# class VMSerializer(BaseSerializer):
#     hypervisor = HypervisorAbstractSerializer(read_only=True)
#     tags = TagAbstractSerializer(many=True, read_only=True)

#     class Meta:
#         model = VM
#         fields = '__all__'


# class XMLDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = XMLData
#         fields = ['xml_type', 'xml_hash', 'raw_xml']