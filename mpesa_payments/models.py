from django.db import models
from transaction.models import BreaderTrade
from django.utils import timezone

class MpesaPayment(models.Model):
    payment_id = models.CharField(max_length=255)  # Add this field to store the PayPal payment ID
    status = models.CharField(max_length=50, default="pending")

    breader_trade = models.ForeignKey(
        BreaderTrade,
        on_delete=models.CASCADE,  # Cascade delete when the associated booking is deleted
        default=None,  # Specify a callable function as the default
        null=True,  # Allow the booking field to be NULL
    )
    is_complete = models.BooleanField(default=False)

    payment_date = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        formatted_date = self.transaction_date.strftime('%d %b %Y %H:%M:%S')  # Adjust the format as needed
        return f"Payment for {self.breader_trade} to {formatted_date}, {self.is_complete}"
          