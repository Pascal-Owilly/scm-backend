# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer
from transaction.models import BreaderTrade
from django.db.models import Sum
from django.http import JsonResponse

class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class BreedCutViewSet(viewsets.ModelViewSet):
    queryset = BreedCut.objects.all()
    serializer_class = BreedCutSerializer


class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer



def total_breeds_supplied(request):
    breeder_totals = BreaderTrade.objects.values('breader__id', 'breed').annotate(total_breed_supply=Sum('breads_supplied'))

    result = []
    for breeder_total in breeder_totals:
        result.append({
            'breeder_id': breeder_total['breader__id'],
            'breed': breeder_total['breed'],
            'total_breed_supply': breeder_total['total_breed_supply'],
        })

    return JsonResponse(result, safe=False)
