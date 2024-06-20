#!/bin/bash

cd pa

python manage.py makemigrations
python manage.py migrate

python fill.py

gunicorn pa.wsgi:application --bind 0.0.0.0:$PORT --log-level debug
