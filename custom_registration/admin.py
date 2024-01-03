from django.contrib import admin
from custom_registration.models import CustomUser, Bank, BankBranch, Status, Payment

admin.site.register(CustomUser)
admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(Status)
admin.site.register(Payment)