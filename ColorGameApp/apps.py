from django.apps import AppConfig
from django.conf import settings
class ColorgameappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ColorGameApp'
    def ready(self):
        from ColorGameApp import scheduler
        scheduler.start()
