from django.contrib import admin
from django.urls import path, include
from apps.kvm.urls import routes as kvm_routes
from apps.common.urls import routes as common_routes
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# router = (common_routes + kvm_routes)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('kvm/', include('apps.kvm.urls')),
    path('term/', include('apps.term.urls')),

    # path("api/", include(router.export), name="api"),
    
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    # index
    path('', include('apps.common.urls')),

]
