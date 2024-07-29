from django.urls import path
from apps.term.views import test
 
urlpatterns = [
    path('test', test, name='test')
]