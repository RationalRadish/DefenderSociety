#!/bin/sh

set -e

. /opt/pysetup/.venv/bin/activate

# Pull all the static files into the root directory for deployment
python manage.py collectstatic --noinput

# Runs the app using uswgsi
uwsgi --socket :8000: --master --enable-threads --module app.wsgi