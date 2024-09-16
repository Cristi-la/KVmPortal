from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.acc.views import SiteTokenObtainPairView
from utils.routes import Route, RouteMap

urlpatterns = [
    path("api/token/", SiteTokenObtainPairView.as_view(), name="token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token.refresh"),
]


routes = RouteMap()