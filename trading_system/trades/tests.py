# trades/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Stock, Trade

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient




@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def stock():
    return Stock.objects.create(id=1, name='Test Stock', price=100)

@pytest.fixture
def api_client(user):
    client = APIClient()
    client.login(username='testuser', password='password')
    return client

@pytest.mark.django_db
def test_create_trade(api_client, stock):
    response = api_client.post('/api/trades/', {
        'user': 1,
        'stock': stock.id,
        'quantity': 10,
        'trade_type': 'BUY'
    })
    assert response.status_code == 201
    assert Trade.objects.count() == 1

@pytest.mark.django_db
def test_total_value(api_client, user, stock):
    Trade.objects.create(user=user, stock=stock, quantity=10, trade_type='BUY')
    Trade.objects.create(user=user, stock=stock, quantity=5, trade_type='BUY')
    response = api_client.get(f'/api/stocks/{stock.id}/value/')
    assert response.status_code == 200
    assert response.data['total_value'] == 1500.0


class TradeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.stock = Stock.objects.create(id=100, name='Test Stock', price=100)

    def test_create_trade(self):
        trade = Trade.objects.create(user=self.user, stock=self.stock, quantity=10, trade_type='BUY')
        self.assertEqual(trade.quantity, 10)
        self.assertEqual(trade.trade_type, 'BUY')

    def test_total_value(self):
        Trade.objects.create(user=self.user, stock=self.stock, quantity=10, trade_type='BUY')
        Trade.objects.create(user=self.user, stock=self.stock, quantity=5, trade_type='BUY')
        trades = Trade.objects.filter(user=self.user, stock=self.stock)
        total_value = sum(trade.quantity * self.stock.price for trade in trades)
        self.assertEqual(total_value, 1500)
