# logistics/views.py
from rest_framework import viewsets
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder
from .serializers import LogisticsStatusSerializer, OrderSerializer, ShipmentProgressSerializer, ArrivedOrderSerializer

class LogisticsStatusViewSet(viewsets.ModelViewSet):
    queryset = LogisticsStatus.objects.all().order_by('-timestamp')
    serializer_class = LogisticsStatusSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date_created')
    serializer_class = OrderSerializer

class ShipmentProgressViewSet(viewsets.ModelViewSet):
    queryset = ShipmentProgress.objects.all().order_by('-timestamp')
    serializer_class = ShipmentProgressSerializer

class ArrivedOrderViewSet(viewsets.ModelViewSet):
    queryset = ArrivedOrder.objects.all().order_by('-timestamp')
    serializer_class = ArrivedOrderSerializer
