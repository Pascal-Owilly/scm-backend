# invoice_generator/views.py
from rest_framework import viewsets
from .models import Invoice, Buyer
from .serializers import InvoiceSerializer, BuyerSerializer
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from .models import Invoice, Buyer, LetterOfCredit
from logistics.models import LogisticsStatus
from .serializers import InvoiceSerializer, BuyerSerializer, LetterOfCreditSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from custom_registration.models import CustomUser
from rest_framework.decorators import action


class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

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

    

class LetterOfCreditViewSet(viewsets.ModelViewSet):
    queryset = LetterOfCredit.objects.all()
    serializer_class = LetterOfCreditSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'pk'  # Ensure this line is present

    def get_queryset(self):
        # Filter letter of credits based on the logged-in user
        return LetterOfCredit.objects.filter(buyer=self.request.user)

    def send_email_notification(self, recipient_email, subject, message):
        send_mail(
            subject,
            message,
            'pascalouma54@gmail.com',  # 
            [recipient_email],
            fail_silently=False,
        )
    print(send_email_notification, 'sent')

    @action(detail=False, methods=['post'])
    def upload_lc_document(self, request, *args, **kwargs):
        try:
            # Retrieve the currently logged-in user
            user = request.user

            user = request.user
            print(f"User: {user}")


            # Create the Letter of Credit
            letter_of_credit = LetterOfCredit.objects.create(user=user, status='pending')

            # Handle LC document upload
            lc_document = request.FILES.get('lc_document')
            letter_of_credit.lc_document = lc_document
            letter_of_credit.save()

            # Notify the buyer and bank about the successful upload
            self.send_lc_upload_notification(letter_of_credit)

            return Response({'message': 'Letter of Credit document uploaded successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error uploading letter of credit document: {e}")
            return Response({'error': 'Error uploading letter of credit document'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_lc_upload_notification(self, letter_of_credit):
        if letter_of_credit.buyer:
            buyer_email = letter_of_credit.buyer.username.email

            # Send email to the buyer
            buyer_subject = 'Letter of Credit Document Uploaded - Processing'
            buyer_message = render_to_string('email_templates/lc_upload_notification_buyer.html', {'letter_of_credit': letter_of_credit})
            self.send_email_notification(buyer_email, buyer_subject, buyer_message)

        # You can also send an email to the bank if needed
        if letter_of_credit.bank_email:
            bank_subject = 'Letter of Credit Document Uploaded - Processing'
            bank_message = render_to_string('email_templates/lc_upload_notification_bank.html', {'letter_of_credit': letter_of_credit})
            self.send_email_notification(letter_of_credit.bank_email, bank_subject, bank_message)

    @action(detail=True, methods=['post'])
    def notify_lc_received(self, request, pk=None):
        letter_of_credit = self.get_object()

        # Check if the letter of credit has an associated invoice
        if letter_of_credit.invoice:
            invoice = letter_of_credit.invoice

            # Check if the invoice has a buyer associated with it
            if invoice.buyer:
                buyer_email = invoice.buyer.username.email

                # Send email to the buyer
                buyer_subject = 'Letter of Credit Received - Processing'
                buyer_message = render_to_string('email_templates/lc_received_notification_buyer.html', {'invoice': invoice})
                self.send_email_notification(buyer_email, buyer_subject, buyer_message)

            # You can also send an email to the bank if needed
            if invoice.bank_email:
                bank_subject = 'Letter of Credit Received - Processing'
                bank_message = render_to_string('email_templates/lc_received_notification_bank.html', {'invoice': invoice})
                self.send_email_notification(invoice.bank_email, bank_subject, bank_message)

        return Response({'message': 'Email notifications sent successfully.'}, status=status.HTTP_200_OK)

def download_invoice_document(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    file_path = invoice.invoice_document.path  # Assuming invoice_document is the FileField    with open(file_path, 'rb') as file:
    response = HttpResponse(file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={invoice.invoice_document.name}'
    return response
        
def download_lc_document(request, lc_id):
    lc = get_object_or_404(LetterOfCredit, id=lc_id)
    file_path = lc.lc_document.path  # Assuming lc_document is the FileField    with open(file_path, 'rb') as file:
    response = HttpResponse(file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={lc.lc_document.name}'
    return response
