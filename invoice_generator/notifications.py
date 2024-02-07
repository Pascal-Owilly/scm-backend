from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

def send_lc_to_the_bank_and_po_to_breeder(instance):
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
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.breeder_trade.breeder.email]

        send_mail(subject, plain_message, from_email, to_email, html_message=message)

        # Additional logic to send emails to BankTeller and CustomerService
        # Replace the following lines with your actual email sending logic

        # Send email to BankTeller
        bank_teller_emails = [bt.user.email for bt in BankTeller.objects.all()]
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
        customer_service_emails = [cs.user.email for cs in CustomerService.objects.all()]
        customer_service_subject = 'Customer Service Notification'

        # Add relevant context for Customer Service
        customer_service_context = {
            'payment': instance,
            'success_message': 'A new payment has been initiated. Please review the details.',
            'additional_info': 'You may need to take further action based on the payment details.',
        }

        # Use customer service email template
        customer_service_message = render_to_string('customer_service_status_email_template.html', customer_service_context)

        send_mail(customer_service_subject, strip_tags(customer_service_message), from_email, customer_service_emails, html_message=customer_service_message)

        return Response({'success': 'Payment processed and notifications sent'}, status=status.HTTP_200_OK)
    else:
        # Handle payment failure, return an appropriate response
        return Response({'error': 'Payment processing failed'}, status=status.HTTP_400_BAD_REQUEST)
