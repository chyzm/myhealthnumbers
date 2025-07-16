#!/bin/bash

echo "🚀 Starting Django app with Gunicorn..."

# Run migrations
echo "🔄 Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if doesn't exist
echo "👑 Attempting to create superuser..."
python manage.py createsuperuser \
  --noinput \
  --username ${DJANGO_SUPERUSER_USERNAME:-admin} \
  --email ${DJANGO_SUPERUSER_EMAIL:-somtochiokaro@gmail.com} \
  --password ${DJANGO_SUPERUSER_PASSWORD:-Legacy@90} 2>/dev/null && echo "✅ Superuser created" || echo "ℹ️ Superuser already exists or creation failed"

# Start Gunicorn server
echo "🌐 Starting Gunicorn server..."
exec gunicorn BMI_calculator.wsgi --bind 0.0.0.0:$PORT