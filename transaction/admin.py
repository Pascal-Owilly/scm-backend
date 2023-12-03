from django.contrib import admin
from transaction.models import  Breader, BreaderTrade, Abattoir, AbattoirPaymentToBreader
# Register your models here.

admin.site.register(BreaderTrade)
admin.site.register(AbattoirPaymentToBreader)
admin.site.register(Breader)
admin.site.register(Abattoir)
