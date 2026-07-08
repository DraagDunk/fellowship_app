#!/bin/sh

# Collect static files
python3 manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate

# Import data
DATA_IMPORT="${DEV_TEST_DATA_PROVISION:-1}"
if [ "$DATA_IMPORT" = "1" ]; then
  if [ ! -e "/fellowship-dev/data-imported" ]; then
    echo "Importing test data"
    python3 manage.py loaddata data/fellowship.json
    touch /fellowship-dev/data-imported
  else
    echo "Test data already imported"
  fi
fi

# Start server
gunicorn --bind 0.0.0.0:8000 --workers 3 --reload fellowship_app.wsgi:application
