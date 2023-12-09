# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer, BreederTotalSerializer
from transaction.models import BreaderTrade
from slaughter_house.models import SlaughterhouseRecord
from django.db.models import Sum, F
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

        # Deduct quantities for slaughtered records
        slaughtered_quantities = (
            SlaughterhouseRecord.objects
            .filter(breed=F('breed'))
            .filter(status='slaughtered')
            .values('breed')
            .annotate(total_slaughtered=Sum('quantity'))
        )

        for breeder_total in breeder_totals:
            breed = breeder_total['breed']
            total_breed_supply = breeder_total['total_breed_supply']

            # Deduct slaughtered quantities if available
            for slaughtered_quantity in slaughtered_quantities:
                if slaughtered_quantity['breed'] == breed:
                    total_breed_supply -= slaughtered_quantity['total_slaughtered']

            breeder_total['total_breed_supply'] = total_breed_supply

        serializer = BreederTotalSerializer(breeder_totals, many=True)

        return Response(serializer.data)