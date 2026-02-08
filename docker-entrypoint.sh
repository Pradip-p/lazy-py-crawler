#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running collectstatic..."
python3 manage.py collectstatic --noinput

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Starting server..."
exec python3 manage.py runserver 0.0.0.0:8000
