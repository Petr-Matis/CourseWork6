import schedule
from django.core.management.base import BaseCommand
import time
from mail_app.services import job


class Command(BaseCommand):
    """Команда для Отправки письма"""
    def handle(self, *args, **options):
        job()
        while True:
            schedule.run_pending()
            timer = 1  # seconds
            time.sleep(timer)
