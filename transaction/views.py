from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Abattoir, Breader, BreaderTrade, AbattoirPaymentToBreader
from .serializers import AbattoirSerializer, BreaderSerializer, BreaderTradeSerializer, AbattoirPaymentToBreaderSerializer
import logging
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Sum
from custom_registration.models import BankTeller, CustomerService
from django.template.loader import render_to_string  # Add this import
from django.utils.html import strip_tags
from django.core.mail import send_mail



class AbattoirViewSet(viewsets.ModelViewSet):
    queryset = Abattoir.objects.all()
    serializer_class = AbattoirSerializer

class BreaderViewSet(viewsets.ModelViewSet):
    queryset = Breader.objects.all()
    serializer_class = BreaderSerializer

logger = logging.getLogger(__name__)

class BreaderTradeViewSet(viewsets.ModelViewSet):

    queryset = BreaderTrade.objects.all().order_by('-transaction_date')
    serializer_class = BreaderTradeSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Log the exception
            logger.error(f"Error in creating BreaderTrade: {str(e)}")
            # Print the error to the console during development
            print(f"Error in creating BreaderTrade: {str(e)}")
            # Return a response indicating the error
            return Response({"error": "An error occurred while creating BreaderTrade."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def breader_info(self, request, pk=None):
        """
        Retrieve detailed information about a specific BreaderTrade.

        Example URL: /api/breader-trade/{pk}/breader-info/
        """
        try:
            breeder_trade = self.get_object()
            breeder_data = BreaderSerializer(breeder_trade.breeder).data
            return Response(breeder_data)
        except Exception as e:
            # Log the exception
            logger.error(f"Error in retrieving Breader information: {str(e)}")
            # Print the error to the console during development
            print(f"Error in retrieving Breader information: {str(e)}")
            # Return a response indicating the error
            return Response({"error": "An error occurred while retrieving Breader information."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def total_quantity(self, request):
        total_quantity_by_breed = BreaderTrade.objects.values('breed').annotate(total_quantity=Sum('breads_supplied'))
        return Response({'total_quantity_by_breed': total_quantity_by_breed})
        print(total_quantity_by_breed)

class BreaderCountView(APIView):
    def get(self, request, format=None):
        breader_count = Breader.objects.count()
        return Response({'breader_count': breader_count}, status=status.HTTP_200_OK)

# class AbattoirPaymentToBreaderViewSet(viewsets.ModelViewSet):
#     queryset = AbattoirPaymentToBreader.objects.all()
#     serializer_class = AbattoirPaymentToBreaderSerializer


# --------------------ABATTOIR PAYMENT TO BREEDER---------
# Payment

class AbattoirPaymentToBreaderViewSet(viewsets.ModelViewSet):
    queryset = AbattoirPaymentToBreader.objects.all()
    serializer_class = AbattoirPaymentToBreaderSerializer

    def create(self, request, *args, **kwargs):
        # Extract the 'breeder_trade_id' from the request data
        breeder_trade_id = request.data.get('breeder_trade_id')

        # Validate the payment data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the payment instance
        payment_instance = serializer.save()

        # If breeder_trade_id is provided, associate the payment with the BreaderTrade
        if breeder_trade_id:
            breeder_trade_instance = BreaderTrade.objects.get(pk=breeder_trade_id)
            payment_instance.breeder_trade = breeder_trade_instance
            payment_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




    def list_payments(self, request, *args, **kwargs):
        # Retrieve all payments
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def process_payment(self):
        # Example: Update payment status to 'Paid'
        self.status = 'payment_initiated'
        self.save()

        # Add additional payment processing logic here
        # For example, interact with a payment gateway, log payment details, etc.

        # Return True if the payment was successful
        return True

    @action(detail=True, methods=['post'])
    def process_payment_and_notify_breeder(self, request, *args, **kwargs):
        instance = self.get_object()

        # Additional logic related to payment details can be performed here
        # For example, check payment status, update related models, log information, etc.

        # Assume the Breeder model has a 'name' field
        breeder_first_name = instance.breeder_trade.breeder.first_name
        breeder_last_name = instance.breeder_trade.breeder.last_name
        breeder_name = f"{breeder_first_name} {breeder_last_name}"

        # Perform the payment processing (replace with your actual payment processing logic)
        success = instance.process_payment()

        if success:
            # Send email to breeder about payment and breeder trade status
            subject = f"Payment and Breeder Trade Code - {instance.payment_code}"

            # Add breeder's name to the context
            context = {
                'payment': instance,
                'success_message': 'You will receive the payment once the processing is complete.',
                'breeder_name': breeder_name,
                'price': instance.breeder_trade.price,
                'payment_initiation_date': instance.payment_initiation_date,
            }

            message = render_to_string('payment_and_breeder_trade_status_email_template.html', context)
            plain_message = strip_tags(message)
            from_email = 'pascalouma54@gmail.com'
            to_email = [instance.breeder_trade.breeder.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=message)

            # Serialize the payment data and return the response
            serializer = self.get_serializer(instance)

            # Additional logic to send emails to BankTeller and CustomerService
            # Replace the following lines with your actual email sending logic

            # Send email to BankTeller
            # Send email to BankTeller
            # Send email to BankTeller
            bank_teller_emails = BankTeller.objects.values_list('user__email', flat=True)
            bank_teller_subject = 'Bank Teller Notification'

            # Add payment code to the context
            bank_teller_context = {
                'payment': instance,
                'success_message': 'Payment has been initiated. Please review the details.',
                'payment_code': instance.payment_code,
            }

            # Use bank teller email template
            bank_teller_message = render_to_string('bank_teller_status_email_template.html', bank_teller_context)

            send_mail(bank_teller_subject, strip_tags(bank_teller_message), from_email, bank_teller_emails, html_message=bank_teller_message)

            # Send email to CustomerService
            customer_service_emails = CustomerService.objects.values_list('user__email', flat=True)
            customer_service_subject = 'Customer Service Notification'

            # Add relevant context for Customer Service
            customer_service_context = {
                'payment': instance,
                'success_message': 'A new payment has been initiated for breeder. Please review the details.',
                'additional_info': 'You may need to take further action based on the payment details.',
            }

            # Use customer service email template
            customer_service_message = render_to_string('customer_service_status_email_template.html', customer_service_context)

            send_mail(customer_service_subject, strip_tags(customer_service_message), from_email, customer_service_emails, html_message=customer_service_message)

            return Response(serializer.data)
        else:
            # Handle payment failure, return an appropriate response
            return Response({'error': 'Payment processing failed'}, status=status.HTTP_400_BAD_REQUEST)

        # Search breeder details by code

    @action(detail=False, methods=['GET'])
    def search_payment_by_code(self, request, *args, **kwargs):
        payment_code = request.query_params.get('payment_code')
        if not payment_code:
            return Response({'error': 'Payment code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Query the database for the payment with the given payment_code
            payment = AbattoirPaymentToBreader.objects.get(payment_code=payment_code)
            
            # Check if the payment is related to a BreaderTrade
            if payment.breeder_trade:
                serializer = AbattoirPaymentToBreaderSerializer(payment)
                return Response(serializer.data)
            else:
                return Response({'error': 'Payment not found or not related to any BreaderTrade'}, status=status.HTTP_404_NOT_FOUND)
        except AbattoirPaymentToBreader.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
# END PAYMENT