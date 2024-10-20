from django.db import models


# --------------------------------------------------------
# Models
# --------------------------------------------------------

class BaseTimeMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseInfoMixin(BaseTimeMixin):
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True



# --------------------------------------------------------
# Fields
# --------------------------------------------------------

class SeparatedCharField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ':') 
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):

        if isinstance(value, list):
            return self.separator.join([str(item) for item in value])
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return value

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return value.split(self.separator)
