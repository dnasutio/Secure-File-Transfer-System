from django.apps import AppConfig
from .encryption.encrypt_file import generate_keys


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    
    def ready(self):
        import api.signals
        # Generate keys if they don't exist
        generate_keys()


    
