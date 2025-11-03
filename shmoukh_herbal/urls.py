# shmoukh_herbal/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView											  
from shmoukh_admin.admin import shmoukh_admin_site
from .health_check import database_health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shmoukh-admin/', shmoukh_admin_site.urls),
    path('', include('products.urls')),
    path('health/', database_health_check, name='health_check'),
    
    # Favicon redirects - fallback for direct requests
    path('favicon.ico', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon/favicon.ico', 
        permanent=True
    )),
    path('favicon-16x16.png', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon/favicon-16x16.png', 
        permanent=True
    )),
    path('favicon-32x32.png', RedirectView.as_view(
        url=settings.STATIC_URL + 'images/favicon/favicon-32x32.png', 
        permanent=True
    )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

