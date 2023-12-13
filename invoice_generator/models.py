# invoice_generator/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES

class Buyer(AbstractUser):
    
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255, default='Example country')
    # Add related names to avoid clashes
    groups = models.ManyToManyField(Group, related_name='buyer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='buyer_permissions')
    
    def __str__(self):

        return self.username

class Invoice(models.Model):
    MEAT_CHOICES = [
        ('chevon', 'Chevon (Goat Meat)'),
        ('mutton', 'mutton'),
        ('beef', 'Beef'),
        ('pork', 'Pork'),
    ]
    breed = models.CharField(max_length=255, choices=MEAT_CHOICES, default='chevon')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='ribs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cut')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)  


    def __str__(self):
        return f'Invoice for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} for {self.buyer.username}  generated on {self.invoice_date}'