FROM    postgres:16.2-bullseye

RUN     apt update -y && apt upgrade -y && \
        apt install locate vim nano lsof curl sudo -y

RUN     mkdir /tools

RUN     pg_createcluster 16 main

COPY    ./conf/postgresql.conf /etc/postgresql/16/main/postgresql.conf

COPY    ./tools/microservice-run.sh /tools/microservice-run.sh

CMD     [ "bash", "tools/microservice-run.sh" ]
