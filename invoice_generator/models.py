from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

CustomUser = get_user_model()

class Buyer(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

class Product(models.Model):
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
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.breed} {self.part_name} - {self.sale_type}'

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product} {self.quantity}'
     
    def total_price(self):
        return self.quantity * self.product.unit_price

class Invoice(models.Model):
    invoice_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    invoice_number = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return f'{self.invoice_number} generated for {self.buyer} containing {self.items} on {self.invoice_date}'

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def save(self, *args, **kwargs):
       if not self.invoice_number:
           base_slug = 'INV'
           timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
           max_existing_invoice_number = Invoice.objects.aggregate(models.Max('invoice_number'))['invoice_number__max']
           if max_existing_invoice_number:
               current_number = int(max_existing_invoice_number.split('-')[-1])
               new_number = current_number + 1
           else:
               new_number = 1
           self.invoice_number = f'{base_slug}-{new_number:03d}-{timestamp}'
       super().save(*args, **kwargs)

    def __str__(self):
        return f'Invoice number #{self.invoice_number} for {self.buyer} - Total Amount: {self.total_amount()}'

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    purchase_order_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    purchase_order_number = models.SlugField(max_length=255, unique=True, editable=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    vendor_notification = models.TextField(blank=True)

    def __str__(self):
        return f'Purchase Order number #{self.purchase_order_number} for {self.buyer} - Status: {self.status}'

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def save(self, *args, **kwargs):
       if not self.purchase_order_number:
           base_slug = 'PO'
           timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
           max_existing_purchase_order_number = PurchaseOrder.objects.aggregate(models.Max('purchase_order_number'))['purchase_order_number__max']
           if max_existing_purchase_order_number:
               current_number = int(max_existing_purchase_order_number.split('-')[-1])
               new_number = current_number + 1
           else:
               new_number = 1
           self.purchase_order_number = f'{base_slug}-{new_number:03d}-{timestamp}'
       super().save(*args, **kwargs)


    def __str__(self):
        return f'Purchase Order number: #{self.purchase_order_number} for {self.buyer} - Status: {self.status}'