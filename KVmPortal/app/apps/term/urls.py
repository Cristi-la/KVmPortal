from django.urls import path, include
from apps.term.views import test, Terminal

urlpatterns = [
    path('test/', test, name='test'),
    path('session/', Terminal.as_view(), name='session'),
]
