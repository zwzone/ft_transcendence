#/bin/bash

python manage.py makemigrations

python manage.py migrate --run-syncdb

if [[ $STAGE == "Deployment" ]]
    then
        daphne -e ssl:8000:privateKey=/etc/ssl/private/ft_transcendence.key:certKey=/etc/ssl/certs/ft_transcendence.crt \
            api.asgi:application
    else
        python manage.py runserver 0.0.0.0:8000
fi
