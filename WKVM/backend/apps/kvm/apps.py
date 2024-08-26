from django.apps import AppConfig


class KvmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.kvm'

    
    def ready(self):
        import apps.kvm.signals