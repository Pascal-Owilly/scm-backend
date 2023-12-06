from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .choices import BREED_CHOICES
from transaction.models import BreaderTrade
from django.db.models import Sum  # Import Sum here

class InventoryBreed(models.Model):
    STATUS_CHOICES = [
        ('in_yard', 'In Yard'),
        ('slaughtered', 'Slaughtered'),
        ('sold', 'Sold'),
    ]

    breed_name = models.CharField(max_length=255, choices=BREED_CHOICES, unique=True, null=True, default='goats')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_yard')
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_breed_name_display()} - Status: {self.get_status_display()}, Quantity: {self.quantity}"


class InventoryBreedSales(models.Model):
    
    SALE_CHOICES = [
        ('export_cuts', 'Export Cuts'),
        ('local_sales_cuts', 'Local Sales Cuts'),
    ]

    PART_CHOICES = [
    ('thighs', 'Thighs'),
    ('ribs', 'Ribs'),
    ('loin', 'Loin'),
    ('shoulder', 'Shoulder'),
    ('shanks', 'Shanks'),
    ('organ_meat', 'Organ Meat'),
    ('intestines', 'Intestines'),
    ('tripe', 'Tripe'),
    ('sweetbreads', 'Sweetbreads'),
]

    breed = models.ForeignKey(InventoryBreed, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='shanks')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.breed} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

class BreedCut(models.Model):
    STATUS_CHOICES = [
        ('in_warehouse', 'In the Warehouse'),
        ('sold', 'Sold'),
    ]

    breed = models.ForeignKey(InventoryBreed, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255, choices=InventoryBreedSales.PART_CHOICES)
    sale_type = models.CharField(max_length=255, choices=InventoryBreedSales.SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    quantity_left = models.PositiveIntegerField(default=0, editable=False)  # Set editable=False to make it read-only in admin
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_warehouse')

    def __str__(self):
        return f"{self.breed} - {self.get_part_name_display()} - {self.get_sale_type_display()} - Status: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self.status == 'sold':
            # Calculate quantity_left based on the total quantity sold
            total_quantity_sold = BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, sale_type=self.sale_type, status='sold').aggregate(Sum('quantity'))['quantity__sum'] or 0
            self.quantity_left = max(self.quantity - total_quantity_sold, 0)

        super().save(*args, **kwargs)

    def quantity_sold(self):
        # Helper method to get the total quantity sold
        return BreedCut.objects.filter(breed=self.breed, part_name=self.part_name, sale_type=self.sale_type, status='sold').aggregate(Sum('quantity'))['quantity__sum'] or 0


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
def update_inventory_breed_quantity(sender, instance, created, **kwargs):
    if created:
        breed_name = instance.breed_name
        try:
            # Use filter instead of get to handle multiple instances
            inventory_breeds = InventoryBreed.objects.filter(breed_name=breed_name)
            
            if inventory_breeds.exists():
                # Assuming you want to update the first instance
                inventory_breed = inventory_breeds.first()
                inventory_breed.quantity += instance.breads_supplied
                inventory_breed.status = 'in_yard'  # Set the status here if needed
                inventory_breed.save()
            else:
                # Create a new InventoryBreed entry if it doesn't exist
                InventoryBreed.objects.create(
                    breed_name=breed_name,
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



