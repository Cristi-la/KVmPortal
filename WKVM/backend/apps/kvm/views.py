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
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from apps.kvm.models import Hypervisor, Tag, XMLData
from apps.kvm.serializers import HypervisorSerializer, TagSerializer, XMLDataSerializer
from rest_framework.exceptions import NotFound

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
    

    # Endpoints:
    # @extend_schema(
    #     responses={200: TagSerializer(many=True)},
    #     description="Retrieve all tags associated with the hypervisor"
    # )
    # @action(detail=True, methods=['get'], url_path='tags', url_name='get_tags')
    # def get_tags(self, request, pk=None):
    #     hypervisor = self.get_object()
    #     tags = hypervisor.tags.all()
    #     serializer = TagSerializer(tags, many=True)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['post'], url_path='tags/add', url_name='add_tag')
    # def add_tag(self, request, pk=None):
    #     hypervisor = self.get_object()
    #     tag_id = request.data.get('tag_id')

    #     try:
    #         tag = Tag.objects.on_current().get(pk=tag_id)
    #     except Tag.DoesNotExist:
    #         raise NotFound("Tag not found")

    #     hypervisor.tags.add(tag)
    #     return Response(TagSerializer(tag).data, status=status.HTTP_200_OK)
    
    # @extend_schema(
    #     request=OpenApiParameter(name="tag_id", type="integer", description="ID of the tag to remove"),
    #     responses={204: OpenApiResponse(description="Tag removed")},
    #     description="Remove a tag from the hypervisor"
    # )
    # @action(detail=True, methods=['post'], url_path='tags/remove', url_name='remove_tag')
    # def remove_tag(self, request, pk=None):
    #     hypervisor = self.get_object()
    #     tag_id = request.data.get('tag_id')

    #     try:
    #         tag = Tag.objects.on_current().get(pk=tag_id)
    #     except Tag.DoesNotExist:
    #         raise NotFound("Tag not found")

    #     hypervisor.tags.remove(tag)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

    @extend_schema(
        parameters=[
            OpenApiParameter(name="xml_type", type={'type': 'string'}, description="Type of the XML data", required=True),
        ],
        responses={200: XMLDataSerializer()},
        description="Retrieve XML data by type for the hypervisor"
    )
    @action(detail=True, methods=['get'], url_path='xml', url_name='get_xml')
    def get_xml(self, request, pk=None):
        hypervisor = self.get_object()
        xml_type = request.query_params.get('xml_type', None)
        import time
        time.sleep(5)
        if not xml_type:
            return Response({"detail": "xml_type is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            xml_data = hypervisor.xmls.get(xml_type=xml_type)
        except XMLData.DoesNotExist:
            raise NotFound("XML data not found")

        return Response(XMLDataSerializer(xml_data).data)


    # @extend_schema(
    #     request=XMLDataSerializer(),
    #     responses={200: XMLDataSerializer()},
    #     description="Set XML data by type for the hypervisor",
    #     parameters=[
    #         OpenApiParameter(name="xml_type", type={'type': 'string'}, description="Type of the XML data", required=True),
    #         OpenApiParameter(name="raw_xml", type={'type': 'string'}, description="Raw XML data", required=True),
    #     ]
    # )
    # @action(detail=True, methods=['post'], url_path='xml', url_name='set_xml')
    # def set_xml(self, request, pk=None):
    #     hypervisor = self.get_object()
    #     xml_type = request.data.get('xml_type')
    #     raw_xml = request.data.get('raw_xml')

    #     if not xml_type or not raw_xml:
    #         return Response({"detail": "xml_type and raw_xml are required"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Process and save the XML data
    #     xml_data, created = XMLData.objects.on_current().update_or_create(
    #         xml_type=xml_type,
    #         defaults={'raw_xml': raw_xml},
    #     )
    #     hypervisor.xmls.add(xml_data)

    #     return Response(XMLDataSerializer(xml_data).data, status=status.HTTP_200_OK)
        

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