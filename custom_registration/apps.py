from django.apps import AppConfig


class CustomRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_registration'



    def ready(self):
        import custom_registration.signals