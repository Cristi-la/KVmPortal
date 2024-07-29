import os
import sys
from celery import Celery
from django.conf import settings
from .celerybeat_schedule import CELERYBEAT_SCHEDULE
from decouple import config

settings_module = config("DJANGO_SETTINGS_MODULE", default='backend.settings')
if settings_module is None:
    print(
        "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
        "Remember to create .env file at project root. "
        "Check README for more info."
    )
    sys.exit(1)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)



app = Celery("backend_tasks")

app.conf.timezone = settings.TIME_ZONE

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
