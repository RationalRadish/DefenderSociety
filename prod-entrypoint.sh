#!/bin/sh

set -e


# Pull all the static files into the root directory for deployment
python manage.py collectstatic --no-input

# Runs the app using uswgsi
uwsgi --master  --ini uwsgi.ini