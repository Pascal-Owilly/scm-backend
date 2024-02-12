# logistics/serializers.py
from rest_framework import serializers
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder, PackageInfo

class PackageInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageInfo
        fields = '__all__'

class LogisticsStatusSerializer(serializers.ModelSerializer):
    # Update the source to use 'id' instead of 'invoice.invoice_number'
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')

    class Meta:
        model = LogisticsStatus
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    # Update the source to use 'id' instead of 'invoice.invoice_number'
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')

    class Meta:
        model = Order
        fields = '__all__'
        
class ShipmentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentProgress
        fields = '__all__'

class ArrivedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivedOrder
        fields = '__all__'
