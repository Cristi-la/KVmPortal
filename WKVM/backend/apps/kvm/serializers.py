from rest_framework import serializers
from apps.kvm.models import Auth, Tag, Hypervisor, VM
from rest_flex_fields import FlexFieldsModelSerializer


# Meta serializers
class VMAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = ['id','name', 'vcpu', 'memory']

class HypervisorAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hypervisor
        fields = ['id', 'hostname', 'mgt_ip']

class TagAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'color']


class BaseSerializer(FlexFieldsModelSerializer):
    ...


# Acuall serializers
class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class HypervisorSerializer(BaseSerializer):
    tags = TagAbstractSerializer(many=True, read_only=True)
    vms = VMAbstractSerializer(many=True, read_only=True)

    class Meta:
        model = Hypervisor
        fields = '__all__'

class VMSerializer(BaseSerializer):
    hypervisor = HypervisorAbstractSerializer(read_only=True)
    tags = TagAbstractSerializer(many=True, read_only=True)

    class Meta:
        model = VM
        fields = '__all__'