from django.contrib import admin
from invoice_generator.models import Invoice, Buyer, LetterOfCredit

admin.site.register(Invoice)
admin.site.register(Buyer)
admin.site.register(LetterOfCredit)