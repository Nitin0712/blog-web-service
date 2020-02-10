from django.apps import AppConfig


class BlogusersConfig(AppConfig):
    name = 'blogusers'

    def ready(self):
        import blogusers.signals