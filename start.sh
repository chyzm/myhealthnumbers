#!/bin/bash

echo "🚀 Starting Django app with Gunicorn..."

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn BMI_calculator.wsgi --bind 0.0.0.0:$PORT
