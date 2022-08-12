from django.core.management.base import BaseCommand
from tg_auth.bot import start_bot


class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **options):
        start_bot()
