# views.py

from rest_framework import viewsets
from .models import Abattoir, Breader, BreaderTrade, AbattoirPayment
from .serializers import AbattoirSerializer, BreaderSerializer, BreaderTradeSerializer, AbattoirPaymentSerializer

class AbattoirViewSet(viewsets.ModelViewSet):
    queryset = Abattoir.objects.all()
    serializer_class = AbattoirSerializer

class BreaderViewSet(viewsets.ModelViewSet):
    queryset = Breader.objects.all()
    serializer_class = BreaderSerializer

class BreaderTradeViewSet(viewsets.ModelViewSet):
    queryset = BreaderTrade.objects.all()
    serializer_class = BreaderTradeSerializer

class AbattoirPaymentViewSet(viewsets.ModelViewSet):
    queryset = AbattoirPayment.objects.all()
    serializer_class = AbattoirPaymentSerializer
