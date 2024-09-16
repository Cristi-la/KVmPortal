import os
import warnings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.kvm.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
                )
            ),
        )
    }
)
