from django.apps import apps
import logging

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .choices import BREED_CHOICES,PART_CHOICES, SALE_CHOICES, STATUS_CHOICES
from transaction.models import BreaderTrade
from django.db.models import Sum  # Import Sum here
from slaughter_house.models import SlaughterhouseRecord

logger = logging.getLogger(__name__)

class BreedCut(models.Model):   
    breed = models.CharField(max_length=255, choices=BREED_CHOICES)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES)
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField(default=0, editable=False)
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_breed_display()} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

    def __str__(self):
        return f"{self.get_breed_display()} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

    def save(self, *args, **kwargs):
        # Calculate total_quantity for the specific part, breed, and sale_type
        total_quantity = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, sale_type=self.sale_type).aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Increment quantity_left by the new value
        self.quantity_left += self.quantity

        # Update quantity based on the calculated total_quantity and new value
        self.quantity = total_quantity + self.quantity

        super().save(*args, **kwargs)


class InventoryBreed(models.Model):

    breed = models.CharField(max_length=255, choices=BREED_CHOICES, default='goats')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='in_yard')

    def __str__(self):
        return f"InventoryBreed - Breed: {self.breed}, Total Breed Supply: {self.total_breed_supply}"

class InventoryBreedSales(models.Model):
    
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

    STATUS_CHOICES = [
        ('in_the warehouse', 'In The Warehouse'),
        ('slaughtered', 'Slaughtered'),
        ('sold', 'Sold'),
    ]

    breed = models.ForeignKey(BreedCut, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='shanks')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.breed.status} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

# @receiver(post_save, sender=InventoryBreedSales)
# def record_breed_cuts(sender, instance, created, **kwargs):
#         if created:
#             breed_cut = BreedCut.objects.create(
#                 breed=instance.breed,
#                 part_name=instance.part_name,
#                 sale_type=instance.sale_type,
#                 quantity=instance.quantity,
#                 sale_date=instance.sale_date
#             )
#             # Update the quantity_left for the associated BreedCut
#             total_quantity_left = breed_cut.manually_add_quantity(0)  # Manually add 0, just to trigger the update
#             print(f"Total Quantity Left: {total_quantity_left}")


# @receiver(post_save, sender=BreaderTrade)
# def update_breads_supplied_quantity(sender, instance, created, **kwargs):
#     if created:
#         breed = instance.breed
#         try:
#             # Use filter instead of get to handle multiple instances
#             breads_supplied = BreedCut.objects.filter(breed=breed)
            
#             if breads_supplied.exists():
#                 # Assuming you want to update the first instance
#                 breads_supplied = breads_supplied.first()
#                 total_quantity_left = breads_supplied.manually_add_quantity(instance.breads_supplied)
#                 print(f"Total Quantity Left: {total_quantity_left}")
#             else:
#                 # Create a new BreedCut entry if it doesn't exist
#                 breed_cut = BreedCut.objects.create(
#                     breed=breed,
#                     part_name='default',  # Set the appropriate default part_name
#                     sale_type='default',  # Set the appropriate default sale_type
#                     quantity=instance.breads_supplied,
#                     sale_date=timezone.now()  # Set the appropriate sale_date
#                 )
#                 # Manually add the specified quantity
#                 total_quantity_left = breed_cut.manually_add_quantity(0)  # Manually add 0, just to trigger the update
#                 print(f"Total Quantity Left: {total_quantity_left}")

#         except ObjectDoesNotExist:
#             pass
