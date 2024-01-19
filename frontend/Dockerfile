FROM		debian:bullseye

RUN			apt update -y && \
			apt upgrade -y && \
			apt install nginx -y

COPY		./conf/nginx.conf /etc/nginx/sites-available/ft_transdance.conf

RUN			mkdir -p /var/www/ft_transcendence/

COPY		. /var/www/ft_transcendence/

CMD			[ "nginx", "-g", "daemon off;" ]

