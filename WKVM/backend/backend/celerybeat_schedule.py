from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "clearsessions": {
        "schedule": crontab(hour=3, minute=0),
        "task": "apps.acc.tasks.clearsessions",
    },
}