from django.urls import re_path
from apps.gui.views import IndexView

urlpatterns = [
    re_path(r".*", IndexView.as_view(), name='main'),
]