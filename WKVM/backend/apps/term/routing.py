from django.urls import re_path
from apps.term.consumers import TermConsumer

websocket_urlpatterns = [
    re_path(r'ws/term/session/(?P<session_id>\d+)/$', TermConsumer.as_asgi()),
]