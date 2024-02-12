cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp

nginx -g 'daemon off;'

if [ $STAGE == "Development" ]
	then
		while true;
		do
			if [ "$(diff /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp)" != "" ] 
				then
				cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp
				service nginx reload
			fi
			sleep 2;
		done
fi
