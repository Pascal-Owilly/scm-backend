from django.contrib import admin
from custom_registration.models import CustomUser, Bank, BankBranch, Status, Payment, CustomerService, BankTeller

admin.site.register(CustomUser)
admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(Status)
admin.site.register(Payment)
admin.site.register(CustomerService)
admin.site.register(BankTeller)