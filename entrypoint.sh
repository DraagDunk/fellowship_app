#!/bin/sh

# Set settings module env variable to allow django-admin to read settings
 export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-fellowship_app.settings}

# Collect static files
django-admin collectstatic --no-input

# Run migrations
django-admin migrate --no-input

# Start server
exec gunicorn --bind 0.0.0.0:8000 --workers 3 fellowship_app.wsgi:application
