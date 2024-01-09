# logistics/serializers.py
from rest_framework import serializers
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder

class LogisticsStatusSerializer(serializers.ModelSerializer):
    # Add a read-only field for displaying the actual invoice number
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')

    class Meta:
        model = LogisticsStatus
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    # Add a read-only field for displaying the actual invoice number
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
