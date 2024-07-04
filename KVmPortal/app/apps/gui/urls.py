from django.urls import path
from apps.gui.views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
]
