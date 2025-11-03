# Create a new file: shmoukh_herbal/signals.py
import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('django.auth')

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    """Send email notification for successful admin logins"""
    if not settings.EMAIL_HOST_USER:
        return
        
    # Only send for admin users
    if user.is_staff or user.is_superuser:
        subject = "Admin Login Notification - Shmoukh Herbal"
        message = f"""
        Successful admin login detected:
        
        User: {user.username}
        Email: {user.email}
        Time: {timezone.now()}
        IP Address: {get_client_ip(request)}
        User Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}
        """
        
        try:
            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMINS[0][1]],
                fail_silently=True,
            )
            logger.info(f"Login notification email sent for {user.username}")
        except Exception as e:
            logger.error(f"Failed to send login notification email: {e}")

@receiver(user_login_failed)
def send_failed_login_alert(sender, credentials, request, **kwargs):
    """Send email alert for failed admin login attempts"""
    if not settings.EMAIL_HOST_USER:
        return
        
    username = credentials.get('username')
    subject = "⚠️ Failed Admin Login Attempt - Shmoukh Herbal"
    message = f"""
    Failed admin login attempt:
    
    Username: {username}
    Time: {timezone.now()}
    IP Address: {get_client_ip(request)}
    User Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}
    
    This could be a security concern if multiple attempts are detected.
    """
    
    try:
        send_mail(
            subject=subject,
            message=message.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMINS[0][1]],
            fail_silently=True,
        )
        logger.info(f"Failed login alert email sent for username: {username}")
    except Exception as e:
        logger.error(f"Failed to send failed login alert email: {e}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
