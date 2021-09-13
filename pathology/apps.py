from django.apps import AppConfig


class PathologyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pathology'
    verbose_name = "病理信息管理"
    def ready(self):
        from . import signals
