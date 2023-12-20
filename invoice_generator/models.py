from django.db import models
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES
from custom_registration.models import CustomUser

class Buyer(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

class Invoice(models.Model):

    MEAT_CHOICES = [
        ('chevon', 'Chevon (Goat Meat)'),
        ('mutton', 'Mutton'),
        ('beef', 'Beef'),
        ('pork', 'Pork'),
    ]
    PART_CHOICES = [
    ('ribs', 'Ribs'),
    ('thighs', 'Thighs'),
    ('loin', 'Loin'),
    ('shoulder', 'Shoulder'),
    ('shanks', 'Shanks'),
    ('organ_meat', 'Organ Meat'),
    ('intestines', 'Intestines'),
    ('tripe', 'Tripe'),
    ('sweetbreads', 'Sweetbreads'),
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
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'Invoice for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} generated on {self.invoice_date}'
