#!/bin/sh

# Collect static files
python3 manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate

# Start server
gunicorn --bind 0.0.0.0:8000 --workers 3 fellowship_app.wsgi:application
