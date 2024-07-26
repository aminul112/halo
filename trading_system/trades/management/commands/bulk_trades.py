import csv
import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trades.models import Stock, Trade
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings


class Command(BaseCommand):
    help = 'Place trades in bulk from a CSV file'

    def handle(self, *args, **kwargs):
        print(settings.CSV_FILE_PATH)
        print(os.path.abspath(os.path.dirname('manage.py')))

        if not settings.CSV_FILE_PATH:
            print("CSV_FILE_PATH is not defined in the settings.py file")

        with open(settings.CSV_FILE_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User.objects.get(username=row['username'])
                try:
                    stock = Stock.objects.get(name=row['stock'])
                except Stock.DoesNotExist:
                    stock = Stock.objects.create(id=row['stock'], name=row['stock_name'], price=row['stock_price'])
                Trade.objects.create(
                    user=user,
                    stock=stock,
                    quantity=row['quantity'],
                    trade_type=row['trade_type']
                )
