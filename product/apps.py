from django.apps import AppConfig
from django.core.signals import request_finished

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    
    def ready(self):
        from . import signals
    