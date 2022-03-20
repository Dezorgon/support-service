#!/bin/sh

until timeout 10 celery --app support inspect ping; do
    >&2 echo "Celery workers not available"
done

celery --app support flower