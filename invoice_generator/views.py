# invoice_generator/views.py
from rest_framework import viewsets
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, status
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from custom_registration.models import CustomUser

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def perform_create(self, serializer):
        try:
            # Check if a buyer is associated with the invoice
            buyer_data = serializer.validated_data.get('buyer', None)

            if buyer_data:
                # If a buyer is provided, create or retrieve the buyer
                user, created = CustomUser.objects.get_or_create(**buyer_data)

                # Update the serializer's buyer field with the CustomUser instance
                serializer.validated_data['buyer'] = user

            # Calculate the total price before saving the object
            serializer.validated_data['total_price'] = (
                serializer.validated_data['quantity'] * serializer.validated_data['unit_price']
            )
            serializer.save()
        except Exception as e:
            print(f"Error in perform_create: {e}")
            raise
        
    # def perform_create(self, serializer):
    #     try:
    #         # Calculate the total price before saving the object
    #         serializer.validated_data['total_price'] = serializer.validated_data['quantity'] * serializer.validated_data['unit_price']
            
    #         # Save the invoice without associating it with a specific buyer
    #         serializer.save()
    #     except Exception as e:
    #         # Handle any exceptions that occur during the creation of the invoice
    #         print(f"Exception occurred: {e}")
    #         raise

    # @action(detail=True, methods=['get'])
    # def get_invoice_ui_data(self, request, pk=None):
    #     invoice = self.get_object()
    #     # Customize the data returned based on your needs
    #     data = {
    #         'flash_message': invoice.flash_message,
    #         'notifications': invoice.notifications,
    #         'purchase_issuance': invoice.purchase_issuance,
    #         'banking_transactions': invoice.banking_transactions,
    #         'cataloging_live_deals': invoice.cataloging_live_deals,
    #         'management_of_deals': invoice.management_of_deals,
    #         'tracking_financed_paid_off_deals': invoice.tracking_financed_paid_off_deals,
    #     }
    #     return Response(data)

    # @action(detail=True, methods=['post'])
    # def update_invoice_actions(self, request, pk=None):
    #     invoice = self.get_object()
    #     # Update boolean fields based on the request data
    #     invoice.purchase_issuance = request.data.get('purchase_issuance', invoice.purchase_issuance)
    #     invoice.banking_transactions = request.data.get('banking_transactions', invoice.banking_transactions)
    #     invoice.cataloging_live_deals = request.data.get('cataloging_live_deals', invoice.cataloging_live_deals)
    #     invoice.management_of_deals = request.data.get('management_of_deals', invoice.management_of_deals)
    #     invoice.tracking_financed_paid_off_deals = request.data.get('tracking_financed_paid_off_deals', invoice.tracking_financed_paid_off_deals)
    #     invoice.save()
    #     return Response(status=status.HTTP_200_OK)


class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer




