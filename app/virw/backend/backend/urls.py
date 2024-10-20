from django.urls import re_path, path, include
from django.contrib import admin
from apps.common.views import DebugView
from apps.private.urls import pub_urls

admin.site.site_header = "VIRW Public Admin"
admin.site.site_title = "VIRW Public Portal"
admin.site.index_title = "Welcome to the VIRW Public admin"

#  ONLY IN PUBLIC SCHEMA
urlpatterns = [
    path('admin/', admin.site.urls),
    path("debug/", DebugView.as_view(), name="debug"),

    *pub_urls,
]

