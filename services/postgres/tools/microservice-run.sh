service postgresql start

adduser $POSTGRES_USER --disabled-password --gecos ""
echo    $POSTGRES_USER:$POSTGRES_PASS | /usr/sbin/chpasswd

echo    "CREATE DATABASE ft_transcendence;" >> postgres.sql
echo    "CREATE USER $POSTGRES_USER WITH ENCRYPTED PASSWORD '$POSTGRES_PASS';" >> postgres.sql
echo    "GRANT ALL PRIVILEGES ON DATABASE ft_transcendence TO $POSTGRES_USER;" >> postgres.sql

sudo    -u postgres psql < postgres.sql


