from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.sites.shortcuts import get_current_site

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class SiteTokenObtainPairSerializer(TokenObtainPairSerializer):
    # def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
    #     data = super().validate(attrs)
    #     request = self.context.get('request')
    #     data['site'] = get_current_site(request).domain
    #     return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token