from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from custom_registration.models import CustomUser, Bank, Seller
from datetime import datetime
import uuid
import random
import string

class Breader(models.Model):

    breeder = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # breeder = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):

        return f'{self.breeder.first_name} {self.breeder.last_name} '

class Abattoir(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    breeders = models.ManyToManyField(Breader, related_name='abattoirs_registered', blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, default=1)

    def __str__(self):

        return f'{self.user.first_name} {self.user.last_name} '

class BreaderTrade(models.Model):
            
    PRODUCTS = []

    breeder = models.ForeignKey(Breader, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    transaction_date = models.DateField(auto_now_add=True)
    breed = models.CharField(max_length=255)
    breeds_supplied = models.PositiveIntegerField(default=0)
    goat_weight = models.PositiveIntegerField(default=0)
    vaccinated = models.BooleanField(default=False, blank=True, null=True)
    email = models.EmailField()
    phone_number = PhoneNumberField(null=True)
    id_number = models.PositiveIntegerField(null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, default=0)
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
        return f"{self.breeder.breeder} supplied {self.breeds_supplied} {self.breed}'s to {self.seller} on {self.created_at}"

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


