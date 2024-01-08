# logistics/serializers.py
from rest_framework import serializers
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder

class LogisticsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsStatus
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
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
