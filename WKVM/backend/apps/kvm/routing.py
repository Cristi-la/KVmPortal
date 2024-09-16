from django.urls import re_path, path
from apps.kvm.consumers import TaskProgressConsumer

websocket_urlpatterns = [
    re_path(r'ws/tasks/$', TaskProgressConsumer.as_asgi()),
]