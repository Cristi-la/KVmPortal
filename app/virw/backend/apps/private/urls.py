
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.private.views import TenantTokenObtainPairView, IndexView
from rest_framework.routers import DefaultRouter
from apps.private.views import StatusViewSet
from apps.private.admin import tenant_site
from apps.common.views import DebugView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r'tags', StatusViewSet, 'tags')


pub_urls = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
]

#  ONLY IN PRIAVTE SCHEMA
urlpatterns = [
    
    path("debug/", DebugView.as_view(), name="debug"),
    path('admin/', tenant_site.urls),
    # path("api/", include(routes.export), name="api"),
    path("api/token/", TenantTokenObtainPairView.as_view(), name="token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token.refresh"),
    path('api/', include('apps.kvm.urls')),

    *pub_urls,
    *router.urls,

    re_path(r".*", IndexView.as_view(), name='index'),
]
