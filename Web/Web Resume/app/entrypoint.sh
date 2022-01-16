#!/bin/sh

#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z $DB_HOST $DB_PORT; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi

: '
To connect to the db:
  1. psql -h localhost -p 5432 -U postgres -w
  2. postgres_db =# \c postgres_db
  3. \dt
'


python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

exec "$@"