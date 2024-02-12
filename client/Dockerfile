FROM		debian:bullseye

RUN			apt update -y && \
			apt upgrade -y && \
			apt install curl vim nano lsof -y && \
			apt install nginx -y

COPY		conf/nginx.conf /etc/nginx/sites-enabled/ft_transcendence.conf

COPY		./private/ssl/certs/ft_transcendence.crt /etc/ssl/certs/ft_transcendence.crt

COPY		./private/ssl/private/ft_transcendence.key /etc/ssl/private/ft_transcendence.key

RUN			mkdir -p /var/www/ft_transcendence/

COPY		. /var/www/ft_transcendence/

CMD			[ "nginx", "-g", "daemon off;" ]

