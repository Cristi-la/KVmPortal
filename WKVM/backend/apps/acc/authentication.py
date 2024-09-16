

from rest_framework_simplejwt.authentication import AuthUser
from rest_framework.exceptions import AuthenticationFailed, ParseError
from apps.common.models import Instance

def account_authentication_rule(user: AuthUser):
    return user is not None and user.is_active and (
        user.is_superuser or \
        user.profile_set.filter(instance=Instance.objects.get_current()).exists() 
    )