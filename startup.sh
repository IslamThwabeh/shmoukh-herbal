#!/bin/bash
# startup.sh

# Run migrations
python manage.py migrate

# Create superuser using our custom command
python manage.py init_superuser

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn shmoukh_herbal.wsgi:application --bind 0.0.0.0:$PORT
