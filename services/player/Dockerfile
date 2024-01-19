FROM        python:3.11.7-bullseye

RUN         apt update -y && \
            apt upgrade -y

RUN         mkdir -p /microservice/player/

COPY        . /microservice/player/

RUN         pip install -r /microservice/player/requirements.txt

WORKDIR     /microservice/player/

CMD         [ "python", "manage.py", "runserver" ]
