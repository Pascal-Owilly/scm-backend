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

# Breed count

class BreederTotalSerializer(serializers.Serializer):
    breeder__id = serializers.IntegerField(source='breader__id')
    breed = serializers.CharField()
    total_breed_supply = serializers.IntegerField()

class BreedCutTotalSerializer(serializers.Serializer):
    part_name = serializers.CharField()
    breed = serializers.CharField()
    quantity = serializers.IntegerField()
    sale_type = serializers.CharField()
    sale_date = serializers.DateField()
    total_breed_cut = serializers.IntegerField()
