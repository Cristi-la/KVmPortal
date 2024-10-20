import os, sys
from decouple import config

settings_module = config("DJANGO_SETTINGS_MODULE", default='backend.conf.local')
if settings_module is None:
    print(
        "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
        "Remember to create .env file at project root. "
        "Check README for more info."
    )
    sys.exit(1)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

from django.conf import settings
from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

app = TenantAwareCeleryApp()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # "all-host-collect-data-task": {
    #     "task": "apps.kvm.tasks.all_host_collect_data",
    #     "schedule": crontab(minute="*/15"),
    # },
    # "simple": {
    #     "task": "apps.kvm.tasks.simple",
    #     "schedule": crontab(minute="*/1"),
    # },
}

app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)









