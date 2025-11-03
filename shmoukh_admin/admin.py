# shmoukh_admin/admin.py
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from products.models import Product, ProductImage

logger = logging.getLogger('shmoukh_admin')

class ShmoukhAdminSite(AdminSite):
    site_header = "Shmoukh Herbal Admin"
    site_title = "Shmoukh Administration"
    index_title = "Welcome to Shmoukh Admin Panel"

    def login(self, request, extra_context=None):
        logger.info(f"Admin login page accessed from IP: {self.get_client_ip(request)}")
        return super().login(request, extra_context)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

shmoukh_admin_site = ShmoukhAdminSite(name='shmoukh_admin')

@admin.register(Product, site=shmoukh_admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock_count', 'is_active']
    list_editable = ['price', 'stock_count', 'is_active']

    def save_model(self, request, obj, form, change):
        if change:
            action = "updated"
            logger.info(f"Product '{obj.name}' updated by {request.user.username}")
        else:
            action = "created"
            logger.info(f"Product '{obj.name}' created by {request.user.username}")
        
        # Send email notification for critical product changes
        self.send_product_notification(request.user, obj, action)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.warning(f"Product '{obj.name}' deleted by {request.user.username}")
        self.send_product_notification(request.user, obj, "deleted")
        super().delete_model(request, obj)

    def send_product_notification(self, user, product, action):
        """Send email notification for product changes"""
        if not settings.EMAIL_HOST_USER:  # Only send if email is configured
            return
            
													 
				  
        subject = f"Product {action.capitalize()}: {product.name}"
        message = f"""
        Product {action} in Shmoukh Herbal Admin:
													  
        
        Product: {product.name}
        Action: {action}
        By User: {user.username}
        Time: {timezone.now()}
        
        Product Details:
        - Price: {product.price}
        - Stock: {product.stock_count}
        - Active: {product.is_active}
        """
        
        try:
            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMINS[0][1]],  # Send to admin email
                fail_silently=True,  # Don't crash if email fails
            )
            logger.info(f"Product {action} notification email sent for '{product.name}'")
        except Exception as e:
            logger.error(f"Failed to send product {action} email: {e}")

@admin.register(ProductImage, site=shmoukh_admin_site)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text']

    def save_model(self, request, obj, form, change):
        if change:
            logger.info(f"Product image for '{obj.product.name}' updated by {request.user.username}")
        else:
            logger.info(f"Product image for '{obj.product.name}' created by {request.user.username}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.warning(f"Product image for '{obj.product.name}' deleted by {request.user.username}")
        super().delete_model(request, obj)
