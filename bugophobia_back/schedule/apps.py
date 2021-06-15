from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = 'schedule'

    def ready(self) -> None:
        import schedule.signals
        return super().ready()
