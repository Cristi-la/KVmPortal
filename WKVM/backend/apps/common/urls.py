from django.urls import re_path, path
from apps.common.views import IndexView
from utils.routes import Route, RouteMap
from apps.common.views import StatusViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from apps.common.views import SiteTokenObtainPairView

urlpatterns = [
    path("api/token/", SiteTokenObtainPairView.as_view(), name="token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token.refresh"),
    re_path(r".*", IndexView.as_view(), name='main'),
]

routes = RouteMap(
    Route(r"status", StatusViewSet,  "status"),
)