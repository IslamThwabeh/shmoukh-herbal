# shmoukh_herbal/middleware.py
import logging
from django.utils import timezone
from django.contrib.auth import get_user_model

logger = logging.getLogger('django.auth')

class AuthenticationLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log login attempts
        if request.path == '/admin/login/' and request.method == 'POST':
            username = request.POST.get('username')
            if hasattr(response, 'status_code'):
                if response.status_code == 302 and response.url == '/admin/':
                    # Successful login
                    logger.info(f"Successful admin login for user: {username} from IP: {self.get_client_ip(request)} at {timezone.now()}")
                elif response.status_code == 200:
                    # Failed login
                    logger.warning(f"Failed admin login attempt for username: {username} from IP: {self.get_client_ip(request)} at {timezone.now()}")
        
        # Log logout events
        elif request.path == '/admin/logout/' and request.method == 'POST':
            if request.user.is_authenticated:
                logger.info(f"User logout: {request.user.username} from IP: {self.get_client_ip(request)} at {timezone.now()}")
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
