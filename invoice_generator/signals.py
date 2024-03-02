from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import LetterOfCredit

@receiver(post_save, sender=LetterOfCredit)
def send_quotation_to_suppliers(sender, instance, created, **kwargs):
    if instance.status == 'approved' and instance.quotation is not None:
        # Ensure instance.quotation is fetched with related data
        quotation = instance.quotation.select_related('seller', 'buyer').first()
        if quotation:
            quotation_content = f"Product: {quotation.product}\nQuantity: {quotation.quantity}\nUnit Price: {quotation.unit_price}\nMessage: {quotation.message}"
            # Send broadcast to suppliers
            suppliers_emails = ['pascalouma54@gmail.com', 'pascalouma55@gmail.com']  # Example list of supplier emails
            subject = 'New Quotation Available'
            message = f'The following quotation is now available:\n\n{quotation_content}'
            send_mail(subject, message, 'pascalouma54@gmail.com', suppliers_emails)
