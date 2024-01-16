# invoice_generator/views.py
from rest_framework import viewsets
from .models import Invoice, Buyer, PurchaseOrder
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import logging

from rest_framework import viewsets, status
from .models import Invoice, Buyer
from logistics.models import LogisticsStatus
from .serializers import InvoiceSerializer, BuyerSerializer, PurchaseOrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from custom_registration.models import CustomUser

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# notify buyer upon each status change

logger = logging.getLogger(__name__)


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

class NotifyBuyerView(APIView):
    def get(self, request, purchase_order_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)

            if purchase_order.status == 'pending':
                # Update the purchase order status to 'under review'
                purchase_order.status = 'under_review'
                purchase_order.save()

                # Notify the buyer
                buyer_message = f"Your purchase order (#{purchase_order.purchase_order_number}) has been received and is under review."

                # Trigger the status_change_signal
                status_change_signal.send(sender=PurchaseOrder, instance=purchase_order)

                # Use your serializer to serialize the purchase order data
                serializer = PurchaseOrderSerializer(purchase_order)

                # Send an email to the buyer
                subject = 'Purchase Order Received and Under Review'
                message = f"Dear {purchase_order.buyer.username},\n\n{buyer_message}\n\nThank you!"
                from_email = 'pascalouma54@gmail.com'  # Replace with your actual email
                to_email = [purchase_order.buyer.username.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)
                logger.info("Email sent successfully")

                return Response({'message': buyer_message, 'purchase_order': serializer.data}, status=status.HTTP_200_OK)
            elif purchase_order.status == 'approved':
                # Add logic for approved status
                purchase_order.status = 'approved'
                purchase_order.save()

                # Notify the buyer
                buyer_message = f"Congratulations! Your purchase order (#{purchase_order.purchase_order_number}) has been approved."

                # Use your serializer to serialize the purchase order data
                serializer = PurchaseOrderSerializer(purchase_order)

                # Send an email to the buyer
                subject = 'Purchase Order Approved'
                message = f"Dear {purchase_order.buyer.username},\n\n{buyer_message}\n\nThank you!"
                from_email = 'pascalouma54@gmail.com'  # Replace with your actual email
                to_email = [purchase_order.buyer.username.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)
                logger.info("Email sent successfully")

                return Response({'message': buyer_message, 'purchase_order': serializer.data}, status=status.HTTP_200_OK)
            elif purchase_order.status == 'declined':
                # Add logic for declined status
                purchase_order.status = 'declined'
                purchase_order.save()

                # Notify the buyer
                buyer_message = f"Unfortunately, your purchase order (#{purchase_order.purchase_order_number}) has been declined."

                # Use your serializer to serialize the purchase order data
                serializer = PurchaseOrderSerializer(purchase_order)

                # Send an email to the buyer
                subject = 'Purchase Order Declined'
                message = f"Dear {purchase_order.buyer.username},\n\n{buyer_message}\n\nThank you for your understanding."
                from_email = 'pascalouma54@gmail.com' 
                to_email = [purchase_order.buyer.username.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)
                logger.info("Email sent successfully")

                return Response({'message': buyer_message, 'purchase_order': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'This purchase order is already under review.'}, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'Purchase Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response({'message': 'Internal Server Error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)