from django.urls import re_path, path
from apps.common.views import IndexView
from utils.routes import Route, RouteMap
from apps.common.views import StatusViewSet
from apps.common.views import DebugView

urlpatterns = [
    path("debug/", DebugView.as_view(), name="debug"),
    re_path(r".*", IndexView.as_view(), name='main'),
]

routes = RouteMap(
    Route(r"status", StatusViewSet,  "status"),
)