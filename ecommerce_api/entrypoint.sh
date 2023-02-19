#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput;

echo "Apply database migrations"
python manage.py makemigrations;
python manage.py migrate;


echo "Create super user"
python manage.py createsuperuser \
    --username=$DJANGO_SUPERUSER_USER \
    --email=$DJANGO_SUPERUSER_USER@email.com \
    --noinput \
    --skip-checks || true

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 --timeout 120 --workers 2 wsgi;