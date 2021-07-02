from django.apps import AppConfig


class LoggerConfig(AppConfig):
    name = 'api.logger'

    def ready(self):
        import api.logger.signals
