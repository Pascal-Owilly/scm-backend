from django.contrib import admin
from invoice_generator.models import Invoice, Buyer

admin.site.register(Invoice)
admin.site.register(Buyer)