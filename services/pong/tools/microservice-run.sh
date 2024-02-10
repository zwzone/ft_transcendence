#/bin/bash

python manage.py makemigrations

python manage.py migrate --run-syncdb

daphne api.asgi:application --port 8000 --bind 0.0.0.0 -v2
