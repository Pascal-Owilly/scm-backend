# logistics/serializers.py
from rest_framework import serializers
from .models import LogisticsStatus, Order, ShipmentProgress, ArrivedOrder, PackageInfo, ControlCenter, CollateralManager
from transaction.serializers import BreaderTradeSerializer

class PackageInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageInfo
        fields = '__all__'

class LogisticsStatusSerializer(serializers.ModelSerializer):
    # Update the source to use 'id' instead of 'invoice.invoice_number'
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')
    buyer_full_name = serializers.CharField(source='get_buyer_full_name', read_only=True)
    seller_full_name = serializers.CharField(source='get_seller_full_name', read_only=True)

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
    assigned_agent_full_name = serializers.CharField(source='get_agent_full_name', read_only=True)
    formatted_created_at = serializers.SerializerMethodField()
    breadertrades = BreaderTradeSerializer(many=True, read_only=True, source='breadertrade_set')  # Include the related BreaderTrade data

    class Meta:
        model = ControlCenter       
        # fields = ['id', 'name', 'address', 'assigned_agent_full_name', 'formatted_created_at', 'breadertrades']
        fields = '__all__'

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%B %d, %Y %I:%M %p')

class CollateralManagerSerializer(serializers.ModelSerializer):
    assigned_agent_full_name = serializers.CharField(source='get_agent_full_name', read_only=True)
    full_name = serializers.CharField(source='get_full_name')
    username = serializers.CharField(source='get_user_name')
    email = serializers.CharField(source='get_user_email')
    address = serializers.CharField(source='get_user_address')
    country = serializers.CharField(source='get_user_country')
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = ControlCenter       
        # fields = ['id', 'name', 'created_at', 'full_name', 'username', 'email', 'address', 'country', 'formatted_created_at']
        fields = '__all__'

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%B %d, %Y %I:%M %p')
