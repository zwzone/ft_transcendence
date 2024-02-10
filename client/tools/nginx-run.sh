nginx -g 'daemon off;'

cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp

while true;
do
    if [ "$(diff /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp)" != "" ] 
    then
        cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp
        service nginx reload
    fi
done
