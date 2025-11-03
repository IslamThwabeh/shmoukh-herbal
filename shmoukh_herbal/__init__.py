# shmoukh_herbal/__init__.py
default_app_config = 'shmoukh_herbal.apps.ShmoukhHerbalConfig'

# shmoukh_herbal/apps.py
from django.apps import AppConfig

class ShmoukhHerbalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shmoukh_herbal'
    
    def ready(self):
        import shmoukh_herbal.signals  # Connect signals
