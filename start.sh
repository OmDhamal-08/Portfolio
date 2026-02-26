#!/usr/bin/env bash
set -o errexit

cd django-portfolio

python manage.py migrate --noinput

gunicorn core.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 3 \
  --worker-class gthread \
  --threads 3 \
  --log-level info \
  --timeout 120 \
  --keep-alive 5