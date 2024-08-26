from rest_framework import serializers
from apps.kvm.models import Auth, Tag, Hypervisor, VM

print(Hypervisor._meta.get_fields())

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

# Acuall serializers
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# Acuall serializers
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class HypervisorSerializer(serializers.ModelSerializer):
    tags = TagAbstractSerializer(many=True, read_only=True)
    vms = VMAbstractSerializer(many=True, read_only=True)

    class Meta:
        model = Hypervisor
        fields = Hypervisor._meta.get_fields()
        fields = ['id', 'hostname', 'mgt_ip', 'tags', 'vms', 'description', 'created', 'updated']


class VMSerializer(serializers.ModelSerializer):
    hypervisor = HypervisorAbstractSerializer(read_only=True)
    tags = TagAbstractSerializer(many=True, read_only=True)

    class Meta:
        model = VM
        fields = '__all__'