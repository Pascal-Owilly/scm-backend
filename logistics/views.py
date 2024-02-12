# logistics/views.py
from rest_framework import viewsets
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder, PackageInfo
from .serializers import LogisticsStatusSerializer, OrderSerializer, ShipmentProgressSerializer, ArrivedOrderSerializer, PackageInfoSerializer
from rest_framework.response import Response
from invoice_generator.models import Buyer
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework import status

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import action
from rest_framework.response import Response

class PackageInfoViewset(viewsets.ModelViewSet):

    queryset = PackageInfo.objects.all()
    serializer_class = PackageInfoSerializer


class LogisticsStatusViewSet(viewsets.ModelViewSet):
    queryset = LogisticsStatus.objects.all().order_by('-timestamp')
    serializer_class = LogisticsStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f"Logistics buyer: {self.request.user}")
        buyer = get_object_or_404(Buyer, buyer=self.request.user)
        return LogisticsStatus.objects.filter(buyer=buyer)

    def retrieve(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')
        instance = get_object_or_404(LogisticsStatus, id=invoice_id)
        print(f"Retrieving logistics status for invoice id: {instance}")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the new status is 'shipped'
        if 'status' in request.data and request.data['status'] == 'shipped':
            # Set the status_updated field to True
            instance.status_updated = True

        serializer.save()

        # Reset status_updated to False after processing the update
        instance.status_updated = False
        instance.save()

        return Response(serializer.data)
        
class LogisticsStatusAllViewSet(viewsets.ModelViewSet):
    queryset = LogisticsStatus.objects.all().order_by('-timestamp')
    serializer_class = LogisticsStatusSerializer

    def retrieve(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')
        instance = get_object_or_404(LogisticsStatus, id=invoice_id)
        print(f"Retrieving logistics status for invoice id: {instance}")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the new status is 'shipped'
        if 'status' in request.data and request.data['status'] == 'shipped':
            # Set the status_updated field to True
            instance.status_updated = True

        serializer.save()

        # Reset status_updated to False after processing the update
        instance.status_updated = False
        instance.save()

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_logistics_and_notify_parties(self, request, *args, **kwargs):
        instance = self.get_object()

        # Additional logic related to logistics update can be performed here
        # For example, check the current status, update related models, log information, etc.

        # Assume the buyer model has a 'name' field
        buyer_name = instance.buyer.name

        # Perform the logistics update (replace with your actual update logic)
        success = instance.update_logistics()

        if success:
            # Send email to buyer about the logistics update
            subject = f"Logistics Update - Order No: {instance.invoice_number}"

            # Add buyer's name to the context
            context = {
                'logistics_status': instance,
                'success_message': 'Logistics status has been updated successfully.',
                'buyer_name': buyer_name,
                'current_status': instance.status,
            }

            message = render_to_string('logistics_update_email_template.html', context)
            plain_message = strip_tags(message)
            from_email = 'pascalouma@gmail.com'  # Replace with your email address
            to_email = [instance.buyer.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=message)

            # Serialize the logistics data and return the response
            serializer = self.get_serializer(instance)

            # Additional logic to send emails to other parties
            # Replace the following lines with your actual email sending logic

            # Send email to AdditionalParty
            additional_party_emails = AdditionalParty.objects.values_list('user__email', flat=True)
            additional_party_subject = 'Additional Party Notification'

            # Add relevant context for AdditionalParty
            additional_party_context = {
                'logistics_status': instance,
                'success_message': 'Logistics status has been updated. Please review the details.',
            }

            # Use AdditionalParty email template
            additional_party_message = render_to_string('buyer_order_arrived.html', additional_party_context)

            send_mail(additional_party_subject, strip_tags(additional_party_message), from_email, additional_party_emails, html_message=additional_party_message)

            return Response(serializer.data)
        else:
            # Handle logistics update failure, return an appropriate response
            return Response({'error': 'Logistics update failed'}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date_created')
    serializer_class = OrderSerializer

class ShipmentProgressViewSet(viewsets.ModelViewSet):
    queryset = ShipmentProgress.objects.all().order_by('-timestamp')
    serializer_class = ShipmentProgressSerializer

class ArrivedOrderViewSet(viewsets.ModelViewSet):
    queryset = ArrivedOrder.objects.all().order_by('-timestamp')
    serializer_class = ArrivedOrderSerializer
