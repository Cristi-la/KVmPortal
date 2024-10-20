
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from drf_spectacular.utils import OpenApiExample, extend_schema
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
<<<<<<< HEAD:app/virw/backend/apps/private/views.py
from apps.private.serializers import MessageSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.private.serializers import TenantTokenObtainPairSerializer


=======
from apps.common.serializers import MessageSerializer
from django.conf import settings
from django.http import HttpRequest, JsonResponse, Http404
from apps.kvm.models import Hypervisor
from apps.kvm.tasks import collect_data

class DebugView(TemplateView):
    template_name = "debug.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not settings.DEBUG:
            raise Http404("This view is only available in debug mode.")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        collect_data.delay(12)


        return super().get(request, *args, **kwargs)
    #     from apps.acc.models import Account
    #     acc = Account.objects.on_current().first()
    #     data = {
    #         "status": "success",
    #         'q': list(acc.profiles.all().values())
    #     }

    #     SingleCollectData.delay()
    #     print('Task scheduled!')

    #     return JsonResponse(data)

>>>>>>> 5547abb4a7464bf1c092df7da4bda8dcd98808dc:WKVM/backend/apps/common/views.py
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
    

