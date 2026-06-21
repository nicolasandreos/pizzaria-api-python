#!/bin/sh

echo "Waiting for database to be ready..."
while ! nc -z mysql 3306; do
    sleep 1
done

echo "Database ready!"

if [ "$RUN_DATABASE_MIGRATIONS" = "true" ]; then
    echo "Applying database migrations..."
    alembic upgrade head
    echo "Database migrations applied!"
fi

if [ "$ENVIRONMENT" = "development" ]; then
    echo "Starting server in development mode..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Starting server in production mode..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000
fi