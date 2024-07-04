from django.urls import path, include
from apps.term.views import test

urlpatterns = [
    path('test/', test, name='test'),
    
]
