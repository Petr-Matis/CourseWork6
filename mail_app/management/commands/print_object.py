from django.core.management.base import BaseCommand
from mail_app.services import print_object


class Command(BaseCommand):
    """Команда для Отправки письма"""
    def handle(self, *args, **options):
        print_object()
