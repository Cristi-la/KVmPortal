# views.py
from rest_framework import viewsets 
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from django.db import models
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import (
    Tag,
    HostDevice,
    StorageVolume,
    NetworkInterface,
    NetworkFilter,
    Snapshot,
    DomainCheckpoint,
    Hypervisor,
    NodeDevice,
    StoragePool,
    Domain,
)
from .serializers import (
    TagSerializer,
    HostDeviceSerializer,
    StorageVolumeSerializer,
    NetworkInterfaceSerializer,
    NetworkFilterSerializer,
    SnapshotSerializer,
    DomainCheckpointSerializer,
    HypervisorSerializer,
    NodeDeviceSerializer,
    StoragePoolSerializer,
    DomainSerializer,
)
from django.http import JsonResponse
import random

# Helper function to get all model fields except 'xml' fields
def get_filterset_fields(model):
    return [
        field.name
        for field in model._meta.get_fields()
        if field.concrete and not field.is_relation and 'xml' not in field.name
    ] + [
        field.name
        for field in model._meta.get_fields()
        if field.is_relation and field.many_to_one or field.one_to_one
    ]

class NonExactFilterSet(FilterSet):
    @classmethod
    def filter_for_field(cls, field, name, lookup_expr='exact'):
        if isinstance(field, (models.CharField, models.TextField)):
            return CharFilter(field_name=name, lookup_expr='icontains')
        elif isinstance(field, models.IntegerField):
            return NumberFilter(field_name=name, lookup_expr='icontains')
        return super().filter_for_field(field, name, lookup_expr)
    
filterBackend = DjangoFilterBackend
filterBackend.filterset_base = NonExactFilterSet

class BaseViewSet(viewsets.ReadOnlyModelViewSet):
    ordering = ['id']
    required_fields = ['id']
    file_name = 'export'
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='fields',
                description='Comma-separated list of fields to include in the output',
                required=False,
                type={'type': 'string'},
            ),
            # OpenApiParameter(
            #     name='export',
            #     description='Format of the exported data (csv, excel, json)',
            #     required=False,
            #     type={'type': 'string'},
            #     enum=['csv', 'excel', 'json'],
            # ),
        ]
    )
    def list(self, request, *args, **kwargs):
        # export_format_param = request.query_params.get('export', None)
        fields_param = request.query_params.get('fields', None)

        if fields_param:
            fields = fields_param.split(',')

            for required_field in self.required_fields:
                if required_field not in fields:
                    fields.append(required_field)
            mutable_query_params = request.query_params.copy()
            mutable_query_params['fields'] = ','.join(fields)
            request._request.GET = mutable_query_params
        return super().list(request, *args, **kwargs)


        # if export_format_param is None:
            

        # queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # data = serializer.data
        # self.file_name =  self.serializer_class.Meta.model.__name__.lower() + '_' + now().strftime('%Y%m%d')

        # if export_format_param == 'csv':
        #     return self.export_csv(data)
        # elif export_format_param == 'excel':
        #     return self.export_excel(data)
        # return self.export_json(data)

    # def export_csv(self, data):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = f'attachment; filename="{self.file_name}.csv"'

    #     if data:
    #         fieldnames = data[0].keys()
    #         writer = csv.DictWriter(response, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerows(data)
    #     return response

    # def export_excel(self, data):
    #     output = io.BytesIO()
    #     df = pd.DataFrame(data)
    #     df.to_excel(output, index=False, engine='xlsxwriter')

    #     response = HttpResponse(
    #         output.getvalue(),
    #         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #     )
    #     response['Content-Disposition'] = f'attachment; filename="{self.file_name}.xlsx"'
    #     return response
    
    # def export_json(self, data):
    #     response = HttpResponse(content_type='application/json')
    #     response['Content-Disposition'] = f'attachment; filename="{self.file_name}.json"'
    #     response.write(json.dumps(data, indent=4))  
    #     return response
    
        

class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering_fields = ['id', 'name']
    filterset_fields = ['id', 'name']
    search_fields = ['name']

class HostDeviceViewSet(BaseViewSet):
    queryset = HostDevice.objects.all()
    serializer_class = HostDeviceSerializer
    ordering_fields = ['id', 'domain', 'node_device']
    filterset_fields = get_filterset_fields(HostDevice)
    search_fields = ['domain__name', 'node_device__name']

class StorageVolumeViewSet(BaseViewSet):
    queryset = StorageVolume.objects.all()
    serializer_class = StorageVolumeSerializer
    ordering_fields = ['id', 'name', 'storage_pool', 'capacity', 'allocation']
    filterset_fields = get_filterset_fields(StorageVolume)
    search_fields = ['name', 'path', 'format_type']

class NetworkInterfaceViewSet(BaseViewSet):
    queryset = NetworkInterface.objects.all()
    serializer_class = NetworkInterfaceSerializer
    ordering_fields = ['id', 'domain', 'mac_address']
    filterset_fields = get_filterset_fields(NetworkInterface)
    search_fields = ['mac_address', 'domain__name', 'model_type']

class NetworkFilterViewSet(BaseViewSet):
    queryset = NetworkFilter.objects.all()
    serializer_class = NetworkFilterSerializer
    ordering_fields = ['id', 'name', 'hypervisor']
    filterset_fields = get_filterset_fields(NetworkFilter)
    search_fields = ['name', 'uuid', 'hypervisor__hostname']

class SnapshotViewSet(BaseViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer
    ordering_fields = ['id', 'name', 'domain']
    filterset_fields = get_filterset_fields(Snapshot)
    search_fields = ['name', 'domain__name', 'state']

class DomainCheckpointViewSet(BaseViewSet):
    queryset = DomainCheckpoint.objects.all()
    serializer_class = DomainCheckpointSerializer
    ordering_fields = ['id', 'name', 'domain']
    filterset_fields = get_filterset_fields(DomainCheckpoint)
    search_fields = ['name', 'domain__name']

class HypervisorViewSet(BaseViewSet):
    queryset = Hypervisor.objects.all()
    serializer_class = HypervisorSerializer
    ordering_fields = ['id', 'hostname', 'mgt_ip']
    filterset_fields = [
        field.name for field in Hypervisor._meta.get_fields()
        if field.concrete and not field.is_relation and 'xml' not in field.name
    ] + ['auth']
    search_fields = ['hostname', 'mgt_ip']

class NodeDeviceViewSet(BaseViewSet):
    queryset = NodeDevice.objects.all()
    serializer_class = NodeDeviceSerializer
    ordering_fields = ['id', 'name', 'hypervisor']
    filterset_fields = [
        field.name for field in NodeDevice._meta.get_fields()
        if field.concrete and not field.is_relation and 'xml' not in field.name and field.name != 'details'
    ] + ['hypervisor']
    search_fields = ['name', 'device_type', 'hypervisor__hostname']

class StoragePoolViewSet(BaseViewSet):
    queryset = StoragePool.objects.all()
    serializer_class = StoragePoolSerializer
    ordering_fields = ['id', 'name', 'hypervisor', 'capacity', 'allocation', 'available']
    filterset_fields = get_filterset_fields(StoragePool)
    search_fields = ['name', 'uuid', 'pool_type', 'hypervisor__hostname']

class DomainViewSet(BaseViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    ordering_fields = ['id', 'name', 'hypervisor', 'state']
    filterset_fields = get_filterset_fields(Domain)
    search_fields = ['name', 'uuid', 'hypervisor__hostname', 'state']