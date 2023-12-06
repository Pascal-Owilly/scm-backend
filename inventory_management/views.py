# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer

class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class BreedCutViewSet(viewsets.ModelViewSet):
    queryset = BreedCut.objects.all()
    serializer_class = BreedCutSerializer


class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer
