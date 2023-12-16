from django.apps import apps
import logging

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from custom_registration.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .choices import BREED_CHOICES,PART_CHOICES, SALE_CHOICES, STATUS_CHOICES
from transaction.models import BreaderTrade
from django.db.models import Sum  # Import Sum here
from slaughter_house.models import SlaughterhouseRecord
from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class BreedCut(models.Model):   
    breed = models.CharField(max_length=255, choices=BREED_CHOICES)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES)
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField(default=0, editable=False)
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_breed_display()} - {self.get_part_name_display()} - {self.get_sale_type_display()} - {self.quantity}"

    # def get_distinct_sales(self):
    #     return self.sales.all().distinct()

    
class InventoryBreed(models.Model):

    breed = models.CharField(max_length=255, choices=BREED_CHOICES, default='goats')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='in_yard')

    def __str__(self):
        return f"InventoryBreed - Breed: {self.breed}, Total Breed Supply: {self.total_breed_supply}"

class InventoryBreedSales(models.Model):
    
    breed = models.ForeignKey(BreedCut, on_delete=models.CASCADE, related_name='sales')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='shanks')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='in_the_warehouse')
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.breed.status} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            try:
                breed_cut = BreedCut.objects.get(id=self.breed_id, part_name=self.part_name, sale_type=self.sale_type)
                breed_cut.quantity -= self.quantity
                breed_cut.save()
                # Update status based on whether the quantity has been deducted
                self.status = 'sold'
            except ObjectDoesNotExist:
                logger.warning(f"BreedCut not found for id={self.breed_id}, part_name={self.part_name}, sale_type={self.sale_type}")
                # Handle the case where the corresponding BreedCut is not found
                # Assuming that status should be 'in_the_warehouse' if not sold
                self.status = 'in_the_warehouse'

        super().save(*args, **kwargs)

class Meta:
    
    unique_together = ['breed', 'part_name', 'sale_type', 'sale_date']