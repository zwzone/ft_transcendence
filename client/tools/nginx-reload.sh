touch   /etc/temp-nginx

inotifywait -q -m -e modify --format %e /etc/nginx/sites-enabled/nginx.conf  |

while read events; do
    echo "changes"
done
