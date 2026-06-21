#!/bin/sh

echo "Applying database migrations..."
if [ "$RUN_DATABASE_MIGRATIONS" = "true" ]; then
    alembic upgrade head
fi

echo "Starting server..."
uvicorn main:app --host 0.0.0.0 --port 8000