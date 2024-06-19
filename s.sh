#!/bin/bash

cd pa

python manage.py makemigrations
python manage.py migrate

python fill.py

kill -9 $(lsof -t -i:8000)

gunicorn pa.wsgi --log-level debug