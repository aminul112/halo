# trades/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Stock, Trade

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def stock():
    return Stock.objects.create(id=1, name="Test Stock", price=100)


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.login(username="testuser", password="password")
    return client


@pytest.mark.django_db
def test_create_trade(api_client, stock):
    assert Trade.objects.count() == 0
    response = api_client.post(
        "/api/trades/",
        {"user": 1, "stock": stock.id, "quantity": 10, "trade_type": "BUY"},
    )
    assert response.status_code == 201
    assert Trade.objects.count() == 1


@pytest.mark.django_db
def test_create_trade_with_unknown_stock(api_client, stock):
    """
    In this test, we are trying to create a trade with a stock id which does not exist
    in our database. So, we must not allow to create a Trade and request must fail.
    """
    assert Trade.objects.count() == 0
    response = api_client.post(
        "/api/trades/",
        {"user": 1, "stock": stock.id + 99, "quantity": 10, "trade_type": "BUY"},
    )
    assert response.status_code == 400
    assert Trade.objects.count() == 0


@pytest.mark.django_db
def test_total_value(api_client, user, stock):
    Trade.objects.create(user=user, stock=stock, quantity=10, trade_type="BUY")
    Trade.objects.create(user=user, stock=stock, quantity=5, trade_type="BUY")
    response = api_client.get(f"/api/stocks/{stock.id}/value/")
    assert response.status_code == 200
    assert response.data["total_value"] == 1500.0


@pytest.mark.django_db
def test_total_value_for_unknown_stock_id(api_client, user, stock):
    """
    In this test we are sending a request to get stock information which does not exist.
    It must fail with error.
    """
    Trade.objects.create(user=user, stock=stock, quantity=10, trade_type="BUY")
    Trade.objects.create(user=user, stock=stock, quantity=5, trade_type="BUY")
    response = api_client.get(f"/api/stocks/9999/value/")
    assert response.status_code == 422
    assert response.data == {"error": "stock id 9999 does not exist!"}


class TradeTestCaseUnit(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.stock = Stock.objects.create(id=100, name="Test Stock", price=100)

    def test_total_value_logic(self):
        Trade.objects.create(
            user=self.user, stock=self.stock, quantity=10, trade_type="BUY"
        )
        Trade.objects.create(
            user=self.user, stock=self.stock, quantity=5, trade_type="BUY"
        )
        trades = Trade.objects.filter(user=self.user, stock=self.stock)
        total_value = sum(trade.quantity * self.stock.price for trade in trades)
        self.assertEqual(total_value, 1500)
