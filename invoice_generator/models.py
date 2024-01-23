from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES
from custom_registration.models import CustomUser
from django.utils import timezone
from datetime import timedelta

class Buyer(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # New field for address
    buyer_email = models.EmailField(editable=True, null=True, blank=True)
    buyer_first_name = models.CharField(max_length=255, editable=True, null=True, blank=True)
    buyer_last_name = models.CharField(max_length=255, editable=True, null=True, blank=True)
    buyer_country = models.CharField(max_length=255, editable=True, null=True, blank=True)
    buyer_phone = models.CharField(max_length=20, editable=True, null=True, blank=True)
    def __str__(self):
        return f'{self.buyer}'

class LetterOfCredit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),

        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='received')

    # File field for storing uploaded documents
    lc_document = models.FileField(upload_to='lc_documents/', null=True, blank=True)

    def __str__(self):
        return f'Letter of Credit #{self.id} from the bank, issued at {self.issue_date} - Status: {self.status} '

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
    due_date = models.DateField(editable=False, null=True, blank=True)

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    
    # File field for storing uploaded documents
    attached_lc_document = models.FileField(upload_to='invoice_documents/', null=False, blank=False)
    
    # Add a SlugField for the invoice number
    invoice_number = models.SlugField(max_length=50, unique=True, editable=False)

    def __str__(self):
        return f'Invoice #{self.invoice_number} for {self.breed} {self.part_name} of type {self.sale_type} - {self.quantity} pieces, generated and sent to {self.buyer} on {self.invoice_date}'

@receiver(pre_save, sender=Invoice)
def pre_save_invoice(sender, instance, **kwargs):
    if not instance.invoice_number:
        # Ensure invoice_date is set correctly, and it's a DateTimeField
        if not instance.invoice_date:
            instance.invoice_date = timezone.now()  # Import timezone from django.utils if not already done

        # Generate a unique slug based on other fields, timestamp, and an incrementing number
        timestamp = instance.invoice_date.strftime('%y%m%d%H%M%S') if instance.invoice_date else 'nodate'
        instance_number = Invoice.objects.count() + 1
        slug = f'{timestamp}-{instance.buyer_id}-{instance_number:05d}'
        instance.invoice_number = slugify(slug)

    # Calculate due date as 30 days from the invoice date
    instance.due_date = instance.invoice_date + timedelta(days=30)

    # Calculate total price based on quantity and unit price
    instance.total_price = instance.quantity * instance.unit_price
