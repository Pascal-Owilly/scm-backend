from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import LogisticsStatus

@receiver(pre_save, sender=LogisticsStatus)
def update_status_handler(sender, instance, **kwargs):
    # Check if the status is being updated
    if instance.status_updated:
        raise ValueError("Status already updated for this order.")

# Signal to send email to buyer when order has arrived
@receiver(post_save, sender=LogisticsStatus)
def send_email_to_buyer(sender, instance, created, **kwargs):
    if created and instance.is_arrived:
        print(f"Sending email to buyer for order {instance.invoice_number}")
        subject = 'Your Order Has Arrived'
        message = render_to_string('email/buyer_order_arrived.html', {'invoice_number': instance.invoice_number})
        plain_message = strip_tags(message)
        from_email = 'pascalouma@gmail.com'  # Remove the extra .com
        to_email = [instance.buyer.email]

        send_mail(subject, plain_message, from_email, to_email, html_message=message)

# Signal to send email to bank when order is received
@receiver(post_save, sender=LogisticsStatus)
def send_email_to_bank(sender, instance, created, **kwargs):
    if created and instance.is_received:
        subject = 'Order Received - Proceed with Payment'
        message = render_to_string('email/bank_order_received.html', {'invoice_number': instance.invoice_number})
        plain_message = strip_tags(message)
        from_email = 'pascalouma@gmail.com.com'  # Replace with your email
        to_email = ['pascal.owilly@gmail.com']  # Replace with actual bank email

        send_mail(subject, plain_message, from_email, to_email, html_message=message)
