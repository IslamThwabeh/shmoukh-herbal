"""
WSGI config for shmoukh_herbal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.db import connection
import logging

logger = logging.getLogger('django')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shmoukh_herbal.settings')

# Log database connection on startup
try:
    application = get_wsgi_application()
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    logger.info("✅ Database connection established successfully")
    db_info = connection.settings_dict
    logger.info(f"📊 Database: {db_info.get('ENGINE')} - {db_info.get('NAME')}")
except Exception as e:
    logger.error(f"❌ Failed to connect to database: {e}")
    raise
