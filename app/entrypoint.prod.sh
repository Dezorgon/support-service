#!/bin/bash

set -o errexit
python manage.py test --noinput
python manage.py collectstatic --noinput
set +o errexit
python manage.py createsuperuser --noinput
gunicorn support.wsgi:application --bind 0.0.0.0:8000

exec "$@"