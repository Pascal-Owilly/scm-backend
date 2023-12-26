from django.db import models
from transaction.models import BreaderTrade, Abattoir

class EquityBankPayment(models.Model):

    breeder_trade = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20, default='pending')  # Set default value
    payer_name = models.ForeignKey(Abattoir, on_delete=models.CASCADE)  # Name of the person making the payment
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Override delete method to prevent deletion
        pass

    def __str__(self):
        return f"Payment of {self.breeder_trade.price} to {self.breeder_trade.breeder} for {self.breeder_trade}  on {self.payment_date}"
