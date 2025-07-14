#!/bin/bash

echo "📣📣📣 SCRIPT STARTED ✅"

echo "✅ Running migrations..."
python manage.py migrate --noinput

echo "✅ Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
gunicorn BMI_calculator.wsgi:application
