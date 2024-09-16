from django.apps import AppConfig


class AccConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.acc'
    verbose_name = 'Account'

    def ready(self):
        import apps.acc.signals