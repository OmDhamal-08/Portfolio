#!/usr/bin/env bash
set -o errexit

cd django-portfolio

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

echo "Build completed successfully."