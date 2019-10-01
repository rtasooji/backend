import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Connecting to database...")
        dp_conn = None
        while not dp_conn:
            try:
                # connecting to Database
                dp_conn = connections['default']
            except OperationalError:
                self.stdout.write("Database unavailable, waiting for 1 second")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
