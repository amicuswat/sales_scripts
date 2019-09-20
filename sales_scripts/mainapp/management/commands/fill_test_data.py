from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fill DB with test data'

    def handle(self, *args, **options):
        pass