#/bin/bash

python manage.py makemigrations

python manage.py migrate --run-syncdb

python manage.py collectstatic --noinput

if [[ $STAGE == "Deployment" ]]
then
    daphne api.asgi:application --port 8000 --bind 0.0.0.0 -v2
else
    python manage.py runserver 0.0.0.0:8000
fi
