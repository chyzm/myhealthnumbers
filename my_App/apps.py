from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_App'


# for signals

def ready(self):
        import my_App.signals