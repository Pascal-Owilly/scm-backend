from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from transaction.models import BreaderTrade
from django.core.exceptions import ObjectDoesNotExist

class InventoryBreed(models.Model):
    
    STATUS_CHOICES = [
        ('in_yard', 'In Yard'),
        ('slaughtered', 'Slaughtered'),
        ('sold', 'Sold'),
    ]

    breed_name = models.CharField(max_length=255, choices=BREED_CHOICES, unique=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_yard')
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_name_display()} - Status: {self.get_status_display()}, Quantity: {self.quantity}"

    def save(self, *args, **kwargs):
        # Set the default status to 'in_yard' when a new breed is added
        if not self.pk:  # Check if it's a new instance
            self.status = 'in_yard'
        super().save(*args, **kwargs)

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
        # Add more choices as needed
    ]

    breed = models.ForeignKey(InventoryBreed, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='thighs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.breed} - {self.get_part_name_display()} - {self.get_sale_type_display()}"

@receiver(pre_save, sender=InventoryBreed)
def adjust_breed_quantity(sender, instance, **kwargs):
    if instance.status == 'in_yard':
        instance.quantity = instance.quantity 
    elif instance.status == 'slaughtered':
        instance.quantity -= 1
    elif instance.status == 'sold':
        instance.quantity -= 1

@receiver(post_save, sender=InventoryBreedSales)
def adjust_sale_quantity(sender, instance, created, **kwargs):
    if created:
        breed = instance.breed
        if instance.sale_type == 'export_cuts':
            breed.quantity -= instance.quantity
        elif instance.sale_type == 'local_sales_cuts':
            breed.quantity += instance.quantity
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
        animal_name = instance.animal_name
        try:
            # Use filter instead of get to handle multiple instances
            inventory_breeds = InventoryBreed.objects.filter(name=animal_name)
            
            if inventory_breeds.exists():
                # Assuming you want to update the first instance
                inventory_breed = inventory_breeds.first()
                inventory_breed.quantity += instance.breads_supplied
                inventory_breed.status = 'in_yard'  # Set the status here if needed
                inventory_breed.save()
            else:
                # Create a new InventoryBreed entry if it doesn't exist
                InventoryBreed.objects.create(
                    name=animal_name,
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
