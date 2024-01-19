# logistics/views.py
from rest_framework import viewsets
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder
from .serializers import LogisticsStatusSerializer, OrderSerializer, ShipmentProgressSerializer, ArrivedOrderSerializer
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

class LogisticsStatusViewSet(viewsets.ModelViewSet):
    queryset = LogisticsStatus.objects.all().order_by('-timestamp')
    serializer_class = LogisticsStatusSerializer

    def retrieve(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')  # Use the correct parameter name

        instance = get_object_or_404(LogisticsStatus, id=invoice_id)
        print(f"Retrieving logistics status for invoice id: {instance}")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date_created')
    serializer_class = OrderSerializer

class ShipmentProgressViewSet(viewsets.ModelViewSet):
    queryset = ShipmentProgress.objects.all().order_by('-timestamp')
    serializer_class = ShipmentProgressSerializer

class ArrivedOrderViewSet(viewsets.ModelViewSet):
    queryset = ArrivedOrder.objects.all().order_by('-timestamp')
    serializer_class = ArrivedOrderSerializer
