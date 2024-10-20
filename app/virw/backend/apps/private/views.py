
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from drf_spectacular.utils import OpenApiExample, extend_schema
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.private.serializers import MessageSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.private.serializers import TenantTokenObtainPairSerializer


class IndexView(TemplateView):
    template_name = "index.html"

class TenantTokenObtainPairView(TokenObtainPairView):
    serializer_class = TenantTokenObtainPairSerializer

    @extend_schema(
        request=TenantTokenObtainPairSerializer,
        responses={
            200: inline_serializer(
                name='TokenRefreshResponse',
                fields={
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField(),
                }
            ),
            400: OpenApiResponse(description='Invalid token or tenant identifier.'),
        },
    )
    def post(self, *args, **kwargs) -> Response:
        return super().post(*args, **kwargs)
    

class StatusViewSet(viewsets.ViewSet):
    serializer_class = MessageSerializer

    @extend_schema(
        summary="Check REST API",
        description="This endpoint checks if the REST API is working.",
        examples=[
            OpenApiExample(
                "Successful Response",
                value={
                    "message": "This message comes from the backend. "
                    "If you're seeing this, the REST API is working!"
                },
                response_only=True,
            )
        ],
        methods=["GET"],
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[AllowAny],
        url_path="rest-check",
    )
    def rest_check(self, request):
        serializer = self.serializer_class(
            data={
                "message": "This message comes from the backend. "
                "If you're seeing this, the REST API is working!"
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

