from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kvm/', include('apps.kvm.urls')),
    path('acc/', include('apps.acc.urls')),
    path('term/', include('apps.term.urls')),

    path('', include('apps.gui.urls')),
]
