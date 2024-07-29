from django.core import management

@celery_app.task
def clearsessions():
    management.call_command("clearsessions")