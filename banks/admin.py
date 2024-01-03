# banks/admin.py
from django.contrib import admin
from .models import Status, Bank, BankBranch, Payment, BankUser, AuditTrail, Currency, DisbursementMode, Alert, Financier, FinancierUser

admin.site.register(Status)
admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(Payment)
admin.site.register(BankUser)
admin.site.register(AuditTrail)
admin.site.register(Currency)
admin.site.register(DisbursementMode)
admin.site.register(Alert)
admin.site.register(Financier)
admin.site.register(FinancierUser)
