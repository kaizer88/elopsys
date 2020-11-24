#!/bin/bash
set -e

if [ "$1" = '/var/django-venv/bin/gunicorn' ]; then
    chown -R app:app /var/lib/celery
    chown -R app:app /var/app
    chown -R app:app /var/media
    /var/django-venv/bin/python /var/app/operations/manage.py migrate --noinput
    /var/django-venv/bin/python /var/app/operations/manage.py collectstatic --noinput
    /var/django-venv/bin/python /var/app/operations/manage.py collectstatic_js_reverse

    STATIC_SRC=`ls /var/static -t | head -1`
    cp /var/static/${STATIC_SRC}/django_js_reverse/js/reverse.js /var/app/operations/statics/js/dj-reverse.js
    exec "$@"
fi

exec "$@"
