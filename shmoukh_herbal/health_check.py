# shmoukh_herbal/health_check.py
import logging
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger('django')

def database_health_check(request):
    """Endpoint to check database connection status"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'engine': connection.settings_dict['ENGINE']
        })
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=500)
