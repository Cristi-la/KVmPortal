#!/bin/bash

set -o errexit
set -o nounset

sleep 30
celery -A backend worker -E --loglevel=DEBUG --pool=solo