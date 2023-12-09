# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer, BreederTotalSerializer
from transaction.models import BreaderTrade
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.response import Response


class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class BreedCutViewSet(viewsets.ModelViewSet):
    queryset = BreedCut.objects.all()
    serializer_class = BreedCutSerializer


class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer



class BreederTotalViewSet(viewsets.ViewSet):

    def list(self, request):
        breeder_totals = (
            BreaderTrade.objects
            .values('breader__id', 'breed')
            .annotate(total_breed_supply=Sum('breads_supplied'))
        )

        serializer = BreederTotalSerializer(breeder_totals, many=True)

        return Response(serializer.data)