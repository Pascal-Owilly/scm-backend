# invoice_generator/models.py
from django.db import models

class Invoice(models.Model):
    part_name = models.CharField(max_length=50)
    sale_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    invoice_date = models.DateField(auto_now_add=True)