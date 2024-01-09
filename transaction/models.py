from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from custom_registration.models import CustomUser
from datetime import datetime
import uuid
import random
import string

class Abattoir(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30)

    def __str__(self):

        return self.user.username

class Breader(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):

        return self.user.username


class BreaderTrade(models.Model):

    BREED_CHOICES = [
        ('goats', 'Goats'),
        ('sheep', 'Sheep'),
        ('cows', 'Cows'),
        ('pigs', 'Pigs'),
        # Add more choices as needed
    ]

    breeder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    abattoir = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    breed = models.CharField(max_length=255, choices=BREED_CHOICES, default='goats')
    breeds_supplied = models.PositiveIntegerField(default=0)
    goat_weight = models.PositiveIntegerField(default=0)
    vaccinated = models.BooleanField(default=False)
    email = models.EmailField()
    phone_number = PhoneNumberField(null=True)
    id_number = models.PositiveIntegerField(null=True)
    bank_account_number = models.CharField(max_length=30, default=1234567891011)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.CharField(max_length=20, unique=True, editable=False)
    # confirmation_code = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique reference when saving the object
        if not self.reference:
            # Use the current date and time if transaction_date is None
            transaction_date = self.transaction_date or datetime.now()
            self.reference = f"{transaction_date.strftime('%y%m%d%H%M')}"

        super().save(*args, **kwargs)

    def __str__(self):
        # formatted_date = self.created_at.strftime('%Y-%m-%d')
        return f"{self.breeder.market} from {self.breeder.community} supplied {self.breeds_supplied} {self.breed}'s to {self.abattoir} on {self.created_at}"
# @receiver(post_save, sender=BreaderTrade)
# def update_breads_supplied(sender, instance, **kwargs):
#     # Update breeds_supplied field after saving   
#     aggregated_sum = BreaderTrade.objects.filter(breader=instance.breader).aggregate(models.Sum('breads_supplied'))['breads_supplied__sum']
#     print(f"Aggregated sum for {instance.breader}: {aggregated_sum}")
#     instance.breads_supplied = aggregated_sum if aggregated_sum is not None else 0
#     instance.save()

# # Connect the signal
# post_save.connect(update_breads_supplied, sender=BreaderTrade)


class AbattoirPaymentToBreader(models.Model):
    SENT_TO_BANK = 'payment_initiated'
    DISBURSED = 'disbursed'
    PAID = 'paid'

    STATUS_CHOICES = [
        (SENT_TO_BANK, 'Sent to Bank for Payment Processing'),
        (DISBURSED, 'Disbursed'),
        (PAID, 'Paid'),
    ]

    payments_id = models.AutoField(primary_key=True)
    breeder_trade = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE)
    # abattoir_payment = models.ForeignKey(BreaderTrade, on_delete=models.CASCADE)

    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_code = models.CharField(max_length=50, unique=True, editable=False)
    payment_initiation_date = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(choices=STATUS_CHOICES, default=SENT_TO_BANK, max_length=100)

    payment_date = models.DateTimeField(auto_now_add=True)

    def process_payment(self):
        # Example: Update payment status to 'Paid'
        self.status = self.SENT_TO_BANK
        self.save()

        # Add additional payment processing logic here
        # For example, interact with a payment gateway, log payment details, etc.

        # Return True if the payment was successful
        return True

    def generate_payment_code(self):
        timestamp_str = datetime.now().strftime('%y%m%d%H%M%S')
        random_chars = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return f"{timestamp_str}{random_chars}"

    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = self.generate_payment_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment to {self.breeder_trade.breeder} for {self.breeder_trade}"