#!/bin/sh

set -e


# Pull all the static files into the root directory for deployment
python manage.py collectstatic --no-input

# Runs the app using uswgsi
gunicorn --workers=3 --bind=0.0.0.0:8000 defender_society.wsgi:application --log-level debug
#uwsgi  --module defender_society.wsgi --http :8000
# --socket defender_society.socket --chmod-socket=666
#uwsgi --ini uwsgi.ini

exec "$@"
