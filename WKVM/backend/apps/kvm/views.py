# views.py
from rest_framework import viewsets 
from apps.kvm.models import Tag, Hypervisor, VM
from apps.kvm.serializers import TagSerializer, HypervisorSerializer, VMSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from django.db import models
import csv
import io
import pandas as pd
from django.http import HttpResponse
import json
from django.utils.timezone import now


class NonExactFilterSet(FilterSet):
    @classmethod
    def filter_for_field(cls, field, name, lookup_expr='exact'):
        if isinstance(field, (models.CharField, models.TextField)):
            return CharFilter(field_name=name, lookup_expr='icontains')
        elif isinstance(field, models.IntegerField):
            return NumberFilter(field_name=name, lookup_expr='startswith')
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
            OpenApiParameter(
                name='export',
                description='Format of the exported data (csv, excel, json)',
                required=False,
                type={'type': 'string'},
                enum=['csv', 'excel', 'json'],
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        export_format_param = request.query_params.get('export', None)
        fields_param = request.query_params.get('fields', None)

        if fields_param:
            fields = fields_param.split(',')

            for required_field in self.required_fields:
                if required_field not in fields:
                    fields.append(required_field)
            mutable_query_params = request.query_params.copy()
            mutable_query_params['fields'] = ','.join(fields)
            request._request.GET = mutable_query_params


        if export_format_param is None:
            return super().list(request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        self.file_name =  self.serializer_class.Meta.model.__name__.lower() + '_' + now().strftime('%Y%m%d')

        if export_format_param == 'csv':
            return self.export_csv(data)
        elif export_format_param == 'excel':
            return self.export_excel(data)
        return self.export_json(data)

    def export_csv(self, data):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.file_name}.csv"'

        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(response, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return response

    def export_excel(self, data):
        output = io.BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(output, index=False, engine='xlsxwriter')

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{self.file_name}.xlsx"'
        return response
    
    def export_json(self, data):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{self.file_name}.json"'
        response.write(json.dumps(data, indent=4))  
        return response
        

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.on_current()
    serializer_class = TagSerializer
    filterset_fields = '__all__'
    search_fields  = ['name']
    pagination_class = None

class HypervisorViewSet(BaseViewSet):
    required_fields = ['id', 'vms']
    queryset = Hypervisor.objects.on_current()
    serializer_class = HypervisorSerializer
    filterset_fields = '__all__'
    search_fields  = ['hostname', 'vms__name']


class VMViewSet(BaseViewSet):
    queryset = VM.objects.on_current()
    serializer_class = VMSerializer
    filterset_fields = '__all__'
    search_fields  = ['id', 'name']