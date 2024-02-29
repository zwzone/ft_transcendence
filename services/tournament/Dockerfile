FROM        python:3.11.7-bullseye

RUN         apt update -y && \
            apt upgrade -y && \
			apt install curl vim nano lsof -y

RUN         mkdir -p /microservice/tournament/

COPY        . /microservice/tournament/

COPY		./private/ssl/certs/ft_transcendence.crt /etc/ssl/certs/ft_transcendence.crt

COPY		./private/ssl/private/ft_transcendence.key /etc/ssl/private/ft_transcendence.key

RUN         pip install --upgrade pip

RUN         pip install -r /microservice/tournament/requirements.txt

WORKDIR     /microservice/tournament/

CMD         [ "bash", "./tools/microservice-run.sh" ]
