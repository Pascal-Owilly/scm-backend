from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from datetime import datetime

CustomUser = get_user_model()

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
    ]

    breed = models.CharField(max_length=255, choices=MEAT_CHOICES, default='chevon')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='ribs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cut')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    
    # Add a SlugField for the invoice number
    invoice_number = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return f'Invoice #{self.invoice_number} for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} pieces, generated and sent to {self.buyer} on {self.invoice_date}'

# Signal to auto-populate the slug field
@receiver(pre_save, sender=Invoice)
def pre_save_invoice(sender, instance, **kwargs):
    if not instance.invoice_number:
        # Generate a unique slug based on an incrementing number and timestamp
        base_slug = 'INV'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        max_existing_invoice_number = Invoice.objects.aggregate(models.Max('invoice_number'))['invoice_number__max']
        if max_existing_invoice_number:
            # Extract the current number and increment it
            current_number = int(max_existing_invoice_number.split('-')[-1])
            new_number = current_number + 1
        else:
            # Start with 1 if no existing invoices
            new_number = 1
        
        # Set the unique invoice_number
        instance.invoice_number = f'{base_slug}-{new_number:03d}-{timestamp}'


# Buyer purchase order and transaction

class Purchase(models.Model):
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
    ]

    # Meat, part, and sale type choices
    breed = models.CharField(max_length=255, choices=MEAT_CHOICES, default='chevon')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='ribs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cut')

    # Purchase details
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Date when the purchase was made
    invoice_date = models.DateField(auto_now_add=True)

    # Buyer information
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    # Link to the original purchase order
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE, null=True, blank=True)

    # Payment status choices
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Purchase #{self.id} for {self.quantity} {self.breed} {self.part_name} ({self.sale_type}), total cost: {self.total_cost}, payment status: {self.payment_status}, made by {self.buyer} on {self.invoice_date}'

# Signal to update total_cost before saving the Purchase model
@receiver(pre_save, sender=Purchase)
def pre_save_purchase(sender, instance, **kwargs):
    # Calculate total cost based on quantity and unit price
    instance.total_cost = instance.quantity * instance.unit_price

class PurchaseOrder(models.Model):
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
    ]

    breed = models.CharField(max_length=255, choices=MEAT_CHOICES, default='chevon')
    part_name = models.CharField(max_length=255, choices=PART_CHOICES, default='ribs')
    sale_type = models.CharField(max_length=255, choices=SALE_CHOICES, default='export_cut')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Link the purchase order to the original invoice
    original_invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    def __str__(self):
        return f'Purchase Order for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} pieces, linked to Invoice #{self.original_invoice.invoice_number}'

# Signal to create a PurchaseOrder when an Invoice is saved
@receiver(pre_save, sender=Invoice)
def create_purchase_order(sender, instance, **kwargs):
    if instance.id is not None:
        # Check if a purchase order already exists for this invoice
        existing_purchase_order = PurchaseOrder.objects.filter(original_invoice=instance)
        if not existing_purchase_order.exists():
            # Create a new purchase order based on the invoice information
            PurchaseOrder.objects.create(
                breed=instance.breed,
                part_name=instance.part_name,
                sale_type=instance.sale_type,
                quantity=instance.quantity,
                unit_price=instance.unit_price,
                original_invoice=instance,
            )