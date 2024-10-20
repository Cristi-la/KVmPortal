from celery import shared_task
from django.db import connection
from backend.celery import app
from tenant_schemas_celery.task import TenantTask
from django_tenants.utils import (
    get_tenant_model,
    tenant_context,
)

@app.task
def my_task():
    print(f'priv {connection.schema_name}',)

@shared_task(base=TenantTask, bind=True)
def my_shared_task(self):
    print(f'shared {connection.schema_name}',)

@app.task
def reset_remaining_jobs_in_public():
    print(f'public job: {connection.schema_name}',)

@app.task
def reset_remaining_jobs_in_all_schemas():
    TenantModel = get_tenant_model()
    
    for tenant in TenantModel.objects.exclude(schema_name='public'):
        with tenant_context(tenant):
            reset_remaining_jobs_in_schema.delay()

@app.task
def reset_remaining_jobs_in_schema():
    print(f'private job: {connection.schema_name}')