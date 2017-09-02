from django.apps import AppConfig

class FdConfig(AppConfig):
    name = 'fd'

    def ready(self):
        import fd.signals
