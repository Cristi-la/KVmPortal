from django.db import models
from apps.acc.models import Account

class Session(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    buffer = models.TextField(blank=True, null=True)
    is_readonly = models.BooleanField(default=True)



class Scripts(models.Model):
    pass


class StickyCommnds(models.Model):
    pass


# - command line[]
# - close session
# - save as flat page
# - share
