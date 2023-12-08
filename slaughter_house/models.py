from django.db import models
from django.contrib.auth.models import User
from .choices import PART_CHOICES, BREED_CHOICES, SALE_CHOICES, STATUS_CHOICES, SALE_CHOICES
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory_management.models import InventoryBreed, InventoryBreedSales
from transaction.models import BreaderTrade

class SlaughterhouseRecord(models.Model):
    breed = models.CharField(max_length=255, choices=BREED_CHOICES, default='goats')
    slaughter_date = models.DateField(auto_now_add=True)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='shanks')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='slaughtered')
    sale_choice = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cuts')

    def __str__(self):
        return f"Slaughterhouse Record - Date: {self.slaughter_date}, Part: {self.get_part_name_display()}, Quantity: {self.quantity}"

    