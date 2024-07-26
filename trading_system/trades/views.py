# trades/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Stock, Trade
from .serializers import StockSerializer, TradeSerializer


class TradeCreateView(generics.CreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TotalValueView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, stock_id):
        user = request.user
        stock = Stock.objects.get(id=stock_id)
        trades = Trade.objects.filter(user=user, stock=stock)
        total_value = sum(trade.quantity * stock.price for trade in trades)
        return Response({"total_value": total_value})
