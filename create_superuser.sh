#!/bin/bash

DJANGO_SUPERUSER_PASSWORD=admin \
python ecommerce_api/manage.py createsuperuser \
    --username=admin \
    --email=admin@email.com \
    --noinput \
    --skip-checks;