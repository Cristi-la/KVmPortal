from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    # durring creation of AUTH_USER_MODEL it is required to comment out this line
    
    path('term/', include('apps.term.urls')),
    path('', include('apps.gui.urls')),



    # Debug toolbar app
    path("__debug__/", include("debug_toolbar.urls")),  
]