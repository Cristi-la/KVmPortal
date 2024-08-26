from typing import Any
from django.contrib.auth.models import UserManager
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query import QuerySet

class AccountManager(UserManager):
    def on_site(self, site=None):
        return self.get_queryset().filter(profile__site=site)
    
    def on_currnet_site(self, site=None):
        return self.get_queryset().filter(profile__site=get_current_site())
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related('profiles')
