cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp

nginx -g 'daemon off;'

if [ $STAGE == "Development" ]
	then
		while true;
		do
			if [ "$(diff /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp)" != "" ] 
				thenclear
				
				service nginx reload
				cp /etc/nginx/sites-enabled/nginx.conf /etc/nginx-config-temp
			fi
		done
fi




