from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    # durring creation of AUTH_USER_MODEL it is required to comment out this line

    path('term/', include('apps.term.urls')),
    path('', include('apps.gui.urls')),



    # Debug toolbar app
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = 'apps.gui.views.handler404'
handler500 = 'apps.gui.views.handler500'
handler403 = 'apps.gui.views.handler403'
handler400 = 'apps.gui.views.handler400'
