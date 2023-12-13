# invoice_generator/views.py
from rest_framework import viewsets
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def perform_create(self, serializer):
        # Calculate the total price before saving the object
        serializer.validated_data['total_price'] = serializer.validated_data['quantity'] * serializer.validated_data['unit_price']
        serializer.save()

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer




