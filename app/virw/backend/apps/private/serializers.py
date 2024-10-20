from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from apps.common.models import TenantUser
from django.db import connection

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: TenantUser):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token["tenant"] = connection.schema_name
        token["is_staff"] = user.is_staff or user.is_superuser

        return token