# trades/management/commands/bulk_trades.py
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from trading_system.trades.models import Stock, Trade


class Command(BaseCommand):
    help = "Place trades in bulk from a CSV file"

    def handle(self, *args, **kwargs):
        with open("path/to/your/csvfile.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User.objects.get(username=row["username"])
                stock = Stock.objects.get(name=row["stock"])
                Trade.objects.create(
                    user=user,
                    stock=stock,
                    quantity=row["quantity"],
                    trade_type=row["trade_type"],
                )
