# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import LetterOfCredit, Quotation

@receiver(post_save, sender=LetterOfCredit)
def send_quotation_to_suppliers(sender, instance, created, **kwargs):
    if instance.status == 'approved':
        quotation = Quotation.objects.get(buyer=instance.buyer)  # Assuming there's only one quotation per buyer
        quotation_content = f"Product: {quotation.product}\nQuantity: {quotation.quantity}\nUnit Price: {quotation.unit_price}\nMessage: {quotation.message}"
        # Send broadcast to suppliers
        suppliers_emails = ['supplier1@example.com', 'supplier2@example.com']  # Example list of supplier emails
        subject = 'New Quotation Available'
        message = f'The following quotation is now available:\n\n{quotation_content}'
        send_mail(subject, message, 'your_email@example.com', suppliers_emails)
