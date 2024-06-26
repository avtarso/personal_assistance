#!/bin/bash
# before running this file
# changing file permissions for execution
# chmod +x first_run.sh

# create virtual enva virtual environment
python3 -m venv paenv

# activate virtual environment
source paenv/bin/activate

# installing required dependencies
pip install -r requirements.txt

# go to the project folder
cd pa

# creating and applying migrations
python manage.py makemigrations
python manage.py migrate

# creating test records
python fill.py

# killing processes using the port 8000
kill -9 $(lsof -t -i:8000)

# starting the server Django
gunicorn pa.wsgi --log-level debug
