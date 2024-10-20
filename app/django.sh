#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py makemigrations
python manage.py migrate_schemas


FLAG_FILE="/app/.create_default_ran"
run_create_default() {
  if [ ! -f "$FLAG_FILE" ]; then
    echo "Running python manage.py create_default..."
    python manage.py create_default
    echo "Command completed. Creating flag file."
    touch "$FLAG_FILE"
  else
    echo "python manage.py create_default has already been run. Skipping."
  fi
}

run_create_default

python manage.py runserver 0.0.0.0:$DJANGO_PORT

# uvicorn backend.asgi:application --host 0.0.0.0 --port $DJANGO_PORT --lifespan off