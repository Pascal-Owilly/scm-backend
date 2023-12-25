# invoice_generator/views.py
from rest_framework import viewsets
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, status
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from custom_registration.models import CustomUser

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-invoice_date')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Check if a buyer is associated with the invoice
            buyer_data = serializer.validated_data.get('buyer', None)
    
            if buyer_data:
                # If a buyer is provided, create or retrieve the buyer
                user, created = CustomUser.objects.get_or_create(**buyer_data)

                # Update the serializer's buyer field with the CustomUser instance
            serializer.validated_data['buyer'] = user  # Use the newly created or retrieved buyer

            # Calculate the total price before saving the object
            serializer.validated_data['total_price'] = (
                serializer.validated_data['quantity'] * serializer.validated_data['unit_price']
            )
            serializer.save()
        except Exception as e:
            print(f"Error in perform_create: {e}")
            raise
        

    def get_queryset(self):
        # Filter invoices based on the logged-in user
        return Invoice.objects.filter(buyer=self.request.user)



class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer




