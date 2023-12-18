from django.db import models
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES
from custom_registration.models import CustomUser

class Buyer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

class Invoice(models.Model):
    MEAT_CHOICES = [
        ('chevon', 'Chevon (Goat Meat)'),
        ('mutton', 'Mutton'),
        ('beef', 'Beef'),
        ('pork', 'Pork'),
    ]
    PART_CHOICES = [
        ('ribs', 'Ribs'),
        ('loin', 'Loin'),
        # Add other part choices as needed
    ]
    SALE_CHOICES = [
        ('export_cut', 'Export Cut'),
        ('local_cut', 'Local Cut'),
        # Add other sale choices as needed
    ]

    breed = models.CharField(max_length=255, choices=MEAT_CHOICES, default='chevon')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='ribs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cut')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    # bill_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bill_to')
    # ship_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ship_to')
    # due_date = models.DateField()

    # Additional fields for UI-related data
    # flash_message = models.TextField(blank=True, null=True)
    # notifications = models.TextField(blank=True, null=True)
    # purchase_issuance = models.BooleanField(default=False)
    # banking_transactions = models.BooleanField(default=False)
    # cataloging_live_deals = models.BooleanField(default=False)
    # management_of_deals = models.BooleanField(default=False)
    # tracking_financed_paid_off_deals = models.BooleanField(default=False)

    def __str__(self):
        return f'Invoice for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} for {self.buyer} generated on {self.invoice_date}'
