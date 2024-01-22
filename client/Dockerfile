FROM		debian:bullseye

RUN			apt update -y && \
			apt upgrade -y && \
			apt install nginx -y

COPY		./conf/nginx.conf /etc/nginx/sites-enabled/ft_transcendence.conf

RUN			mkdir -p /var/www/ft_transcendence/

COPY		. /var/www/ft_transcendence/

CMD			[ "sleep", "1000000" ]

