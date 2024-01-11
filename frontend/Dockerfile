FROM debian:latest

# COPY ./ /var/www/Javascript

RUN apt update -y && \
  apt upgrade -y && \
  apt install nginx -y
# mv /var/www/Javascript/nginx.conf /etc/nginx/conf.d/

COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 81

CMD [ "nginx", "-g", "daemon off;" ]
