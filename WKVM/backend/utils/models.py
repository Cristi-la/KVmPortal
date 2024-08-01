from django.db import models


class BaseTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseInfo(BaseTime):
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True