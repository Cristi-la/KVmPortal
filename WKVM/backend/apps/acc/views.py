from rest_framework.request import Request
from rest_framework.response import Response
from apps.acc.serializers import SiteTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class SiteTokenObtainPairView(TokenObtainPairView):
    serializer_class = SiteTokenObtainPairSerializer

    # @extend_schema(
    #     methods=["POST"],
    #     responses={
    #         property: {}
    #     }
    # )
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
