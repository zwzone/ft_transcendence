FROM        python:3.11.7-bullseye

RUN         apt update -y && \
            apt upgrade -y && \
			apt install curl vim nano lsof -y

RUN         mkdir -p /microservice/player/

COPY        . /microservice/player/

COPY		./private/ssl/certs/ft_transcendence.crt /etc/ssl/certs/ft_transcendence.crt

COPY		./private/ssl/private/ft_transcendence.key /etc/ssl/private/ft_transcendence.key

RUN         pip install --upgrade pip

RUN         pip install -r /microservice/player/requirements.txt

WORKDIR     /microservice/player/

CMD         [ "bash", "./tools/microservice-run.sh" ]
