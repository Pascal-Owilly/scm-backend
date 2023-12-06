from django.db import models
from django.contrib.auth.models import User
from .choices import PART_CHOICES  # Import the choices file where PART_CHOICES is defined
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory_management.models import InventoryBreed


class SlaughterhouseRecord(models.Model):
    slaughter_date = models.DateField(auto_now_add=True)
    part_name = models.CharField(max_length=255, choices=PART_CHOICES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Slaughterhouse Record - Date: {self.slaughter_date}, Part: {self.get_part_name_display()}, Quantity: {self.quantity}"


@receiver(post_save, sender=SlaughterhouseRecord)
def update_inventory_on_slaughter(sender, instance, created, **kwargs):
    if created:
        part_name = instance.part_name
        try:
            # Use filter instead of get to handle multiple instances
            inventory_breeds = InventoryBreed.objects.filter(inventorybreedsales__part_name=part_name)

            if inventory_breeds.exists():
                # Assuming you want to update the first instance
                inventory_breed = inventory_breeds.first()
                inventory_breed.quantity += instance.quantity
                inventory_breed.status = 'in_yard'  
                inventory_breed.save()
            else:
                # Create a new InventoryBreed entry if it doesn't exist
                InventoryBreed.objects.create(
                    part_name=part_name,
                    quantity=instance.quantity,
                    status='in_yard'  
                )
        except models.ObjectDoesNotExist:
            pass