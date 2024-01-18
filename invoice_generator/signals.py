# invoice_generator/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import PurchaseOrder
from django.db.models.signals import Signal

status_change_signal = Signal()


@receiver(post_save, sender=PurchaseOrder)
def send_email_on_status_change(sender, instance, **kwargs):
    if kwargs.get('created', False):  # Skip if it's a new instance
        return

    # Check if the status field has changed
    if instance.status != instance._original_status:
        # Notify the buyer
        subject = f'Purchase Order Status Change: {instance.status}'
        message = f"Dear {instance.buyer.username},\n\nYour purchase order (#{instance.purchase_order_number}) has been updated.\n\nStatus: {instance.status}\n\nThank you!"
        from_email = 'pascalouma54@gmail.com'  # Replace with your actual email
        to_email = [instance.buyer.username.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Update the original status to the current status for the next comparison
        instance._original_status = instance.status
