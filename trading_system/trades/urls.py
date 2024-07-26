# trades/urls.py
from django.urls import path
from .views import TradeCreateView, TotalValueView

urlpatterns = [
    path("trades/", TradeCreateView.as_view(), name="create-trade"),
    path("stocks/<int:stock_id>/value/", TotalValueView.as_view(), name="total-value"),
]
