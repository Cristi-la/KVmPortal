#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'

sleep 30
celery -A backend beat --loglevel=DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A backend beat --loglevel=INFO --scheduler backend.scheduler:ReadyTenantAwareScheduler