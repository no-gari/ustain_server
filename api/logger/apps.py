from django.apps import AppConfig


class LoggerConfig(AppConfig):
    name = 'api.logger'
    verbose_name = '발송 기록'

    def ready(self):
        import api.logger.signals
