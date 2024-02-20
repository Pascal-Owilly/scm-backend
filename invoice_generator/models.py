from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES
from custom_registration.models import CustomUser, Bank
from django.utils import timezone
from datetime import timedelta
from transaction.models import Abattoir, Breader
from custom_registration.models import Seller
# ---------------Seller Purchase order--------------------------------------------

class PurchaseOrder(models.Model):
    
    # Header Information
    seller = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    trader_name = models.ForeignKey(Breader, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    confirmed = models.BooleanField(default=False)
    
    # Line Items
    product_description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Terms and Conditions
    delivery_terms = models.CharField(max_length=255)

    # Additional Information
    special_instructions = models.TextField()

    def __str__(self):
        return f'purchase order from {self.seller} created on {self.date}'

    #-------------Seller LC------------------------------------------------

class LetterOfCreditSellerToTrader(models.Model):
    # Header Information

   
    # Terms and Conditions
    # Define choices for shipment periods
    SHIPMENT_PERIODS = [
        ('immediate', 'Immediate'),
        ('within_30_days', 'Within 30 Days'),
        ('within_60_days', 'Within 60 Days'),
        # Add more choices as needed
    ]
    shipment_period = models.CharField(max_length=20, choices=SHIPMENT_PERIODS, default='immediate')

    # Define choices for documents required
    DOCUMENTS_REQUIRED_CHOICES = [
        ('invoice', 'Invoice'),
        ('packing_list', 'Packing List'),
        ('bill_of_lading', 'Bill of Lading'),
        # Add more choices as needed
    ]
    documents_required = models.TextField(choices=DOCUMENTS_REQUIRED_CHOICES, default='bill_of_lading')

    # Define choices for approval statuses
    APPROVAL_STATUSES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUSES, default='pending')

    # Define choices for tracking statuses
    TRACKING_STATUSES = [
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('delayed', 'Delayed'),
    ]
    tracking_status = models.CharField(max_length=20, choices=TRACKING_STATUSES, default='in_transit')

    seller = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    breeder = models.ForeignKey(Breader, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    lc_number = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    beneficiary_name = models.CharField(max_length=255)
    beneficiary_address = models.TextField()
    issuing_bank_name = models.CharField(max_length=255)
    issuing_bank_address = models.TextField()
    advising_bank_name = models.CharField(max_length=255)
    advising_bank_address = models.TextField()

    # Terms and Conditions
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    shipment_period = models.CharField(max_length=100)
    documents_required = models.TextField()
    special_conditions = models.TextField()

    # Payment Information
    payment_at_sight = models.BooleanField(default=False)
    deferred_payment = models.BooleanField(default=False)
    payment_terms = models.CharField(max_length=255)

    # Additional Information
    reference_numbers = models.CharField(max_length=255)
    attachments = models.FileField(upload_to='lc_from_local_seller_to_local_trader/', blank=True, null=True)

    # Approval and Signature
    authorized_signature_issuing_bank = models.CharField(max_length=255)
    authorized_signature_advising_bank = models.CharField(max_length=255)
    signature_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.lc_number
        
    #-------------End Seller LC--------------------------------------------

# ---------------Profoma invoice from traser to seller

class ProformaInvoiceFromTraderToSeller(models.Model):
    # Header Information
    invoice_number = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    seller = models.ForeignKey(Abattoir, on_delete=models.CASCADE)
    buyer_address = models.TextField()
    trader = models.ForeignKey(Breader, on_delete=models.CASCADE)
    seller_address = models.TextField()

    # Line Items
    product_description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Terms and Conditions
    payment_terms = models.CharField(max_length=255)
    delivery_terms = models.CharField(max_length=255)

    # Additional Information
    reference_numbers = models.CharField(max_length=255)
    attachments = models.FileField(upload_to='invoices_from_local_traders_to_local_sellers/', blank=True, null=True)


    def __str__(self):
        return f'Invoice #{self.invoice_number} for {self.seller.first_name} - {self.date}'

#--------------------- End profoma-------------------------------------

# ----------------End Seller-----------------------------------------------


# ----------------Buyer----------------------------------------------------

class Buyer(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_full_name(self):
        if self.buyer:
            return f'{self.buyer.first_name} {self.buyer.last_name}'
        return "Unknown"

    def get_user_name(self):
        if self.buyer:
            return self.buyer.username
        return "Unknown"

    def get_user_email(self):
        if self.buyer:
            return self.buyer.email
        return "Unknown"

    def get_user_country(self):
        if self.buyer:
            return self.buyer.country
        return "Unknown"

    def get_user_address(self):
        if self.buyer:
            return self.buyer.address
        return "Unknown"

    def __str__(self):
        if self.buyer:
            return self.buyer.username
        return "Unknown"


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

# -------------------End Buyer---------------------------------------------------------------------------------

# Buyer and quotation

class Quotation(models.Model):

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)  # Updated field name
    confirm = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()  # Updated field name
    delivery_time = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Updated field name
    message = models.TextField()  # Updated field name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quotation for {self.product} by {self.buyer}"
