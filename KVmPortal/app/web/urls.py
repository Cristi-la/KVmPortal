from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('term/', include('apps.term.urls')),
    path('', include('apps.gui.urls')),



    # Debug toolbar app
    path("__debug__/", include("debug_toolbar.urls")),
]
