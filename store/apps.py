from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'
from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'  # apni app ka naam yahan likho

    def ready(self):
        import store.signals  # apni app ka naam yahan bhi