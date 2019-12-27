from django.apps import AppConfig


class GetchappConfig(AppConfig):
    name = 'getchapp'

    def ready(self):
        import getchapp.signals
