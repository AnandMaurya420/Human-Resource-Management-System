from django.apps import AppConfig


class LeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Leave'

    def ready(self):
        import Leave.signals