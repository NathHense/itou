#!/bin/sh
set -e

while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

# # https://github.com/docker/compose/issues/1926#issuecomment-422351028
# trap : TERM INT
# tail -f /dev/null & wait

django-admin migrate

# --nopin disables for you the annoying PIN security prompt on the web
# debugger. For local dev only of course!
django-admin runserver_plus 0.0.0.0:8000 --nopin

exec "$@"
