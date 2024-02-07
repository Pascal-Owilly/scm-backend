from django.contrib import admin
from invoice_generator.models import Invoice, Buyer, LetterOfCredit, PurchaseOrder, LetterOfCreditSellerToTrader

admin.site.register(Invoice)
admin.site.register(Buyer)
admin.site.register(LetterOfCredit)
admin.site.register(PurchaseOrder)
admin.site.register(LetterOfCreditSellerToTrader)
