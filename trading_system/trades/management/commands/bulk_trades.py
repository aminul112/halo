import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from trades.models import Stock, Trade
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings


class Command(BaseCommand):
    help = "Place trades in bulk from a CSV file"

    def handle(self, *args, **kwargs):
        # print(settings.CSV_FILE_PATH)
        # print(os.path.abspath(os.path.dirname('manage.py')))

        if not settings.CSV_FILE_PATH:
            raise CommandError("CSV_FILE_PATH is not defined in the settings.py file")

        with open(settings.CSV_FILE_PATH, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    user = User.objects.get(username="test")
                except User.DoesNotExist:
                    error = f"User {row['username']} does not exist in our database. Quiting!"
                    raise CommandError(error)
                try:
                    stock = Stock.objects.get(name=row["stock"])
                except Stock.DoesNotExist:
                    print("Stock does not exist, creating a new stock.")
                    stock = Stock.objects.create(
                        id=row["stock"],
                        name=row["stock_name"],
                        price=row["stock_price"],
                    )
                Trade.objects.create(
                    user=user,
                    stock=stock,
                    quantity=row["quantity"],
                    trade_type=row["trade_type"],
                )
