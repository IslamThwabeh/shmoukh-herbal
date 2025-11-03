# shmoukh_herbal/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shmoukh_admin.admin import shmoukh_admin_site
from .health_check import database_health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shmoukh-admin/', shmoukh_admin_site.urls),
    path('', include('products.urls')),
    path('health/', database_health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
