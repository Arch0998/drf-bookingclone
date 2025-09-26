import os
import time

import psycopg2
from django.core.management import BaseCommand
from psycopg2 import OperationalError


class Command(BaseCommand):
    help = "Waits for the database to be available."
    
    def handle(self, *args, **options):
        db_host = os.environ["POSTGRES_HOST"]
        db_name = os.environ["POSTGRES_DB"]
        db_user = os.environ["POSTGRES_USER"]
        db_pass = os.environ["POSTGRES_PASSWORD"]
        db_port = os.environ["POSTGRES_PORT"]
        while True:
            try:
                conn = psycopg2.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_pass,
                    host=db_host,
                    port=db_port,
                )
                conn.close()
                self.stdout.write(self.style.SUCCESS("Database is ready!"))
                break
            except OperationalError:
                self.stdout.write("Waiting for database...", ending="\r")
                time.sleep(1)
