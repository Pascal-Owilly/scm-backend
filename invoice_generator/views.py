# invoice_generator/views.py
from rest_framework import generics
from .models import Invoice
from .serializers import InvoiceSerializer

class GenerateInvoiceView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def perform_create(self, serializer):
        # Calculate the total price before saving the object
        serializer.validated_data['total_price'] = serializer.validated_data['quantity'] * serializer.validated_data['unit_price']
        serializer.save()