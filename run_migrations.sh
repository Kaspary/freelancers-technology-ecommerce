#!/bin/bash

python ecommerce_api/manage.py makemigrations;
python ecommerce_api/manage.py migrate;