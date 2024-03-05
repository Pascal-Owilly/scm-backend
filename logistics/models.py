# logistics/models.py
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from invoice_generator.models import Invoice, Buyer, Seller
from custom_registration.models import CustomUser
# from transaction.models import BreaderTrade
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES

# Control centers

class CollateralManager(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    associated_seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_full_name(self):
        return f'{self.name.first_name} {self.name.last_name}' if self.name else "No  manager assigned"

    def get_associated_seller_full_name(self):
        return self.associated_seller.get_full_name() if self.associated_seller else "No seller assigned"

    def get_user_name(self):
        if self.name:
            return self.name.username
        return "Unknown"

    def get_user_email(self):
        if self.name:
            return self.name.email
        return "Unknown"    

    def get_user_country(self):
        if self.name:
            return self.name.country
        return "Unknown"

    def get_user_address(self):
        if self.name:
            return self.name.address
        return "Unknown"

    def __str__(self):
        if self.name:
            return self.name.username
        return "Unknown"

    def __str__(self):
        return self.name.username if self.name else "Unnamed Collateral Manager"

class ControlCenter(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    assigned_collateral_agent = models.ForeignKey(CollateralManager, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def get_agent_full_name(self):
        if self.assigned_collateral_agent:
            return self.assigned_collateral_agent.get_full_name()
        else:
            return "No assigned collateral agent"

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.order_number} for user {self.buyer} - {self.status}"

class ShipmentProgress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status} - Order #{self.order.order_number}'

class ArrivedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Arrived - Order #{self.order.order_number}'

class PackageInfo(models.Model):

    package_name = models.CharField(max_length=255, null=True, blank=True)
    package_description = models.CharField(max_length=255, null=True, blank=True)
    package_charge = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    length = models.CharField(max_length=255, null=True, blank=True)
    bill_of_lading=models.FileField(upload_to='bill_of_landings', null=True, blank=True)

    def __str__(self):
        return self.package_name

class LogisticsStatus(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('arrived', 'Arrival'),
        ('received', 'Received'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    # time_of_delivery = models.DateField(null=True, blank=True)
    shipping_mode = models.CharField(max_length=255, null=True, blank=True)
    logistics_company = models.CharField(max_length=255, null=True, blank=True)
    associated_control_center = models.ForeignKey(ControlCenter, on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="ordered")
    package_info = models.ForeignKey(PackageInfo, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_status_updated = models.BooleanField(default=False)

    def get_seller_full_name(self):
        try:
            return f'{self.seller.seller.first_name} {self.seller.seller.last_name}'
        except AttributeError:
            return None

    def get_buyer_full_name(self):
        try:
            return f'{self.buyer.buyer.first_name} {self.buyer.buyer.last_name}'
        except AttributeError:
            return None


    
    def save(self, *args, **kwargs):
        # Populate buyer and seller from the associated invoice
        if not self.buyer or not self.seller:
            invoice = self.invoice
            if invoice:
                self.buyer = invoice.buyer
                self.seller = invoice.seller
        super().save(*args, **kwargs)

    


    @property       
    def is_arrived(self):
        return self.status == 'arrived'

    @property
    def is_received(self):
        return self.status == 'received'


    def __str__(self):
        return f'{self.status} - {self.invoice}'

