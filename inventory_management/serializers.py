# serializers.py

from rest_framework import serializers
from .models import InventoryBreed, InventoryBreedSales, BreedCut

class InventoryBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryBreed
        fields = '__all__'

class InventoryBreedSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryBreedSales
        fields = '__all__'

class BreedCutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreedCut
        fields = '__all__'
