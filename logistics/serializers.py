# logistics/serializers.py
from rest_framework import serializers
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder, PackageInfo, ControlCenter, CollateralManager

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

class ControlCenterSerializer(serializers.ModelSerializer):
    assiged_agent_full_name = serializers.CharField(source='get_agent_full_name', read_only=True)
        
    class Meta:
        model = ControlCenter       
        fields = '__all__'

class CollateralManagerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    associated_seller_full_name = serializers.CharField(source='get_associated_seller_full_name', read_only=True)

    class Meta:
        model = CollateralManager
        fields = ['id', 'full_name', 'associated_seller_full_name']