from django.apps import apps

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

class BreedCut(models.Model):   

    breed = models.CharField(max_length=255, choices=BREED_CHOICES)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES)
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField(default=0, editable=False)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_warehouse')

    def __str__(self):
        return f"{self.get_breed_display()} - {self.get_part_name_display()} - {self.get_sale_type_display()} - Status: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self.status == 'in_warehouse':
            # Update quantity_left based on total quantity of the specific part for the breed cuts
            total_quantity = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, status='in_warehouse').aggregate(Sum('quantity'))['quantity__sum'] or 0
            self.quantity_left = total_quantity + self.quantity

            # If it's a new local sales part, add to the local sales quantity
            if self.sale_type == 'local_sales_cuts':
                local_sales_quantity = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, sale_type='local_sales_cuts', status='in_warehouse').aggregate(Sum('quantity'))['quantity__sum'] or 0
                self.quantity_left += local_sales_quantity
            # If it's a new export part, add to the export quantity
            elif self.sale_type == 'export_cuts':
                export_quantity = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, sale_type='export_cuts', status='in_warehouse').aggregate(Sum('quantity'))['quantity__sum'] or 0
                self.quantity_left += export_quantity

        elif self.status == 'sold':
            # Adjust quantity_left when the specific part of breed cuts are sold
            total_quantity_sold = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, status='sold').aggregate(Sum('quantity'))['quantity__sum'] or 0
            self.quantity_left = max(total_quantity - total_quantity_sold, 0)

        super().save(*args, **kwargs)

class InventoryBreed(models.Model):
    breed = models.CharField(max_length=255, choices=BreaderTrade.BREED_CHOICES, default='goats')
    total_quantity = models.PositiveIntegerField(default=0)

    def update_total_quantity(self):
        # Update total quantity based on BreaderTrade records
        total_breads_supplied = BreaderTrade.objects.filter(breed=self.breed).aggregate(total_breads_supplied=models.Sum('breads_supplied'))['total_breads_supplied'] or 0

        # Calculate the total quantity
        self.total_quantity = total_breads_supplied
        self.save()

    def __str__(self):
        return f"InventoryBreed - Breed: {self.breed}, Total Quantity: {self.total_quantity}"

# Signal to update InventoryBreed when a BreaderTrade is saved
@receiver(post_save, sender=BreaderTrade)
def update_inventory_breed(sender, instance, **kwargs):
    # Assuming InventoryBreed has a ForeignKey to BreaderTrade named 'breader_trade'
    # Adjust the following line based on your actual ForeignKey field
    breads_supplied = instance.breader.user.username

    if breads_supplied:
        breads_supplied.update_total_quantity()
        
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


@receiver(pre_save, sender=InventoryBreed)
def adjust_breed_quantity(sender, instance, **kwargs):
    if instance.status == 'in_yard':
        # Only adjust the quantity if the status is 'in_yard'
        instance.quantity = instance.quantity
    elif instance.status == 'slaughtered':
        instance.quantity -= 1
    elif instance.status == 'sold':
        instance.quantity -= 1

@receiver(post_save, sender=InventoryBreed)
def update_inventory_breed_quantity(sender, instance, **kwargs):
    if instance.status == 'in_yard':
        # Adjust the quantity only if the status is 'in_yard'
        instance.quantity += 1
    elif instance.status == 'slaughtered':
        instance.quantity -= 1
    elif instance.status == 'sold':
        instance.quantity -= 1

@receiver(post_save, sender=InventoryBreedSales)
def record_breed_cuts(sender, instance, created, **kwargs):
    if created:
        breed = instance.breed
        if instance.sale_type == 'export_cuts' or instance.sale_type == 'local_sales_cuts':
            # Create a BreedCut instance for each sold part
            BreedCut.objects.create(
                breed=breed,
                part_name=instance.part_name,
                sale_type=instance.sale_type,
                quantity=instance.quantity,
                sale_date=instance.sale_date
            )

@receiver(post_save, sender=InventoryBreedSales)
def adjust_sale_quantity(sender, instance, created, **kwargs):
    if created:
        breed = instance.breed
        if instance.sale_type == 'export_cuts':
            breed.quantity -= instance.quantity
        elif instance.sale_type == 'local_sales_cuts':
            breed.quantity -= instance.quantity  # Adjust the quantity by subtracting for local sales
        breed.save()

# Additional signal to update quantity when InventoryBreedSales is updated
@receiver(pre_save, sender=InventoryBreedSales)
def update_sale_quantity(sender, instance, **kwargs):
    # Check if the quantity is being updated (not created)
    if instance.pk is not None:
        breed = instance.breed
        # Adjust the breed quantity by subtracting the previous quantity
        breed.quantity -= instance.quantity

@receiver(post_save, sender=BreaderTrade)
def update_breads_supplied_quantity(sender, instance, created, **kwargs):
    if created:
        breed = instance.breed
        try:
            # Use filter instead of get to handle multiple instances
            breads_supplied = BreedCut.objects.filter(sales__part_name=part_name)
            
            if breads_supplied.exists():
                # Assuming you want to update the first instance
                breads_supplied = breads_supplied.first()
                breads_supplied.quantity += instance.breads_supplied
                breads_supplied.status = 'in_yard'  # Set the status here if needed
                breads_supplied.save()
            else:
                # Create a new InventoryBreed entry if it doesn't exist
                InventoryBreed.objects.create(
                    breed=breed,
                    quantity=instance.breads_supplied,
                    status='in_yard'  # Set the status here if needed
                )
        except ObjectDoesNotExist:
            pass

@receiver(post_save, sender=InventoryBreedSales)
def update_breader_trade(sender, instance, created, **kwargs):
    if created:
        breed = instance.breed
        if instance.sale_type == 'export_cuts':
            breed.quantity -= instance.quantity
        elif instance.sale_type == 'local_sales_cuts':
            breed.quantity += instance.quantity

        # Ensure quantity is not less than 0
        breed.quantity = max(breed.quantity, 0)

        breed.save()



