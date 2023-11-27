from django.contrib import admin
from transaction.models import  Breader, BreaderTrade, Abattoir, AbattoirPayment
# Register your models here.

admin.site.register(BreaderTrade)
admin.site.register(AbattoirPayment)
admin.site.register(Breader)
admin.site.register(Abattoir)
