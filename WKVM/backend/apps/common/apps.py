from django.apps import AppConfig
from django.conf import settings

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'


    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(self.create_instance, sender=self)

    def create_instance(self, sender, **kwargs):
        from apps.common.models import Instance

        if settings.SITE_ID is None:
            return
        
        obj, _ = Instance.objects.update_or_create(id=settings.SITE_ID)
        obj.domain = 'localhost'
        obj.name = 'root'
        obj.save()
        


