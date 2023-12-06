# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer

class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer
