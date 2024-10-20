

from rest_framework_simplejwt.authentication import AuthUser
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import connection
from apps.common.models import TenantUser
from django.core.cache import cache

def account_authentication_rule(user: TenantUser) -> bool:
    if user is None or not user.is_active:
        return False

    tenant = connection.tenant

    if tenant is None:
        return False

    return user.tenants.filter(id=tenant.id).exists()

class TenantJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if auth := super().authenticate(request):
            user, token = auth
            if token.payload["tenant"] == connection.schema_name:
                return user, token
        return None