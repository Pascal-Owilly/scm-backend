from django.db import models
from django.contrib.auth.models import User
from .choices import PART_CHOICES, BREED_CHOICES, SALE_CHOICES, STATUS_CHOICES, SALE_CHOICES
from django.db.models.signals import post_save
from django.dispatch import receiver
# from inventory_management.models import InventoryBreed, InventoryBreedSales
# from transaction.models import BreaderTrade
from logistics.models import ControlCenter

class SlaughterhouseRecord(models.Model):

    SLAUGHTER_STATUS_CHOICES = [
            ('slaughtered', 'Slaughtered'),
    ]

    breed = models.CharField(max_length=255, null=True, blank=True, default='goats')
    slaughter_date = models.DateField(auto_now_add=True)
    # part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='shanks')
    quantity = models.PositiveIntegerField()
    confirm = models.BooleanField(default=False)  # Confirm that the record is correct before saving it to
    control_center = models.ForeignKey(ControlCenter, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=SLAUGHTER_STATUS_CHOICES, default='slaughtered')
    # sale_choice = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cuts')
    weight = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return f"Slaughterhouse Record - Date: {self.slaughter_date}, Quantity: {self.quantity}"


    