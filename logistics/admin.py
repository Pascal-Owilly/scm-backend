# logistics/admin.py
from django.contrib import admin
from .models import LogisticsStatus, PackageInfo, ControlCenter, CollateralManager

admin.site.register(LogisticsStatus)
admin.site.register(PackageInfo)
admin.site.register(ControlCenter)
admin.site.register(CollateralManager)


