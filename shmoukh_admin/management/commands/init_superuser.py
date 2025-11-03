# shmoukh_admin/management/commands/init_superuser.py
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
import os

logger = logging.getLogger('shmoukh_admin')

class Command(BaseCommand):
    help = 'Create superuser if it does not exist'

    def handle(self, *args, **options):
        # Log database connection info
        db_info = connection.settings_dict
        logger.info(f"Database configuration:")
        logger.info(f"  Engine: {db_info.get('ENGINE', 'Unknown')}")
        logger.info(f"  Name: {db_info.get('NAME', 'Unknown')}")
        logger.info(f"  User: {db_info.get('USER', 'Unknown')}")
        logger.info(f"  Host: {db_info.get('HOST', 'Unknown')}")
        logger.info(f"  Port: {db_info.get('PORT', 'Unknown')}")

        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                logger.info("✅ Database connection test: SUCCESS")
        except Exception as e:
            logger.error(f"❌ Database connection test: FAILED - {e}")
            return

        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        logger.info(f"Superuser environment variables:")
        logger.info(f"  Username: {'Set' if username else 'Not set'}")
        logger.info(f"  Email: {'Set' if email else 'Not set'}")
        logger.info(f"  Password: {'Set' if password else 'Not set'}")

        if not all([username, email, password]):
            logger.warning('Superuser environment variables not set. Skipping superuser creation.')
            self.stdout.write(
                self.style.WARNING('Superuser environment variables not set. Skipping superuser creation.')
            )
            return

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                logger.info(f'Superuser {username} created successfully!')
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser {username} created successfully!')
                )
            else:
                logger.info(f'Superuser {username} already exists.')
                self.stdout.write(
                    self.style.WARNING(f'Superuser {username} already exists.')
                )
        except Exception as e:
            logger.error(f"Failed to create superuser: {e}")
            self.stdout.write(
                self.style.ERROR(f'Failed to create superuser: {e}')
            )
