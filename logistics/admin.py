# logistics/admin.py
from django.contrib import admin
from .models import LogisticsStatus, PackageInfo

admin.site.register(LogisticsStatus)
admin.site.register(PackageInfo)


