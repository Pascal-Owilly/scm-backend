from rest_framework import serializers
from inventory_management.models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Inventory
        fields = '__all__'