#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations polls --no-input -v 0
python manage.py migrate --no-input

exec "$@"