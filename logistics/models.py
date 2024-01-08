# logistics/models.py
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from invoice_generator.models import Invoice
from custom_registration.models import CustomUser
from inventory_management.choices import BREED_CHOICES, PART_CHOICES, SALE_CHOICES

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

class LogisticsStatus(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('arrived', 'Arrival'),
        ('received', 'Received'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status} - {self.invoice}'
