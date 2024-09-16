from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.acc.models import Account

class SiteTokenObtainPairSerializer(TokenObtainPairSerializer):
    # def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
    #     data = super().validate(attrs)
    #     request = self.context.get('request')
    #     data['site'] = get_current_site(request).domain
    #     return data

    @classmethod
    def get_token(cls, user: Account):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_admin'] = user.is_staff or user.is_superuser
        token['profiles'] = list(user.prof)

        return token