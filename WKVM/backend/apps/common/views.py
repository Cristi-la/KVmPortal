from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView, View
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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

class IndexView(TemplateView):
    template_name = "index.html"


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