# trades/models.py
from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Trade(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TRADE_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trade_type} {self.quantity} of {self.stock.name}'
