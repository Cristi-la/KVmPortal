# views.py
from rest_framework import viewsets 
from apps.kvm.models import Tag, Hypervisor, VM
from apps.kvm.serializers import TagSerializer, HypervisorSerializer, VMSerializer
# from drf_spectacular. import DetailSerializerMixin

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class HypervisorViewSet(viewsets.ModelViewSet):
    queryset = Hypervisor.objects.all()
    serializer_class = HypervisorSerializer

class VMViewSet(viewsets.ModelViewSet):
    queryset = VM.objects.all()
    serializer_class = VMSerializer