#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations polls --no-input -v 0
python manage.py migrate --no-input

if [ "${DJANGO_SUPERUSER_NAME}" ]; then
  python manage.py create_admin \
          --username "${DJANGO_SUPERUSER_USERNAME}" \
          --email "${DJANGO_SUPERUSER_EMAIL}" \
          --password "${DJANGO_SUPERUSER_PASSWORD}"
fi

exec "$@"