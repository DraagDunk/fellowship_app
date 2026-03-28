#!/bin/sh

# Load environment variables from .env (if needed)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
npx sequelize-cli db:migrate || {
  echo "Migration failed. Exiting..."
  exit 1
}

echo "Starting the app..."
exec "$@"
