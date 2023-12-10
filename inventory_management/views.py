# views.py

from rest_framework import viewsets
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer, BreederTotalSerializer, BreedCutTotalSerializer
from transaction.models import BreaderTrade
from slaughter_house.models import SlaughterhouseRecord
from django.db.models import Sum, F, Case, When, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Count


class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class BreedCutViewSet(viewsets.ModelViewSet):
    queryset = BreedCut.objects.all()
    serializer_class = BreedCutSerializer

class BreedCutTotalViewSet(viewsets.ViewSet):

    def list(self, request):
        # Calculate total breed cut for each part_name
        breed_cut_totals = (
            BreedCut.objects
            .values('breed','part_name', 'quantity', 'sale_type', 'sale_date')
            .annotate(total_breed_cut=Sum('quantity'))
        )

        # Convert the queryset to a list
        cut_totals = list(breed_cut_totals)

        # Ensure all entries have 'part_name' key
        for entry in cut_totals:
            entry['part_name'] = entry.get('part_name', None)

        serializer = BreedCutTotalSerializer(cut_totals, many=True)

        return Response(serializer.data)


class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer

class BreederTotalViewSet(viewsets.ViewSet):

    def list(self, request):
        # Calculate total breed supply from BreaderTrade
        breeder_totals = (
            BreaderTrade.objects
            .values('breader__id', 'breed')
            .annotate(total_breed_supply=Sum('breads_supplied'))
        )

        # Calculate total slaughtered from SlaughterhouseRecord
        slaughtered_quantities = (
            SlaughterhouseRecord.objects
            .values('breed')
            .annotate(total_slaughtered=Sum('quantity'))
        )

        # Combine both results into a dictionary for easy access
        total_dict = {}
        for total in breeder_totals:
            breader_id = total['breader__id']
            breed = total['breed']
            total_dict.setdefault(breed, {'breader__id': breader_id, 'total_breed_supply': 0, 'breed': breed})
            total_dict[breed]['total_breed_supply'] += total['total_breed_supply']

        for slaughtered_quantity in slaughtered_quantities:
            breed = slaughtered_quantity['breed']
            total_dict.setdefault(breed, {'breader__id': None, 'total_breed_supply': 0, 'breed': breed})
            
            # Check if breed exists in breeder_totals before subtracting
            if breed in total_dict:
                # Validate before subtracting
                remaining_breed_supply = total_dict[breed]['total_breed_supply'] - slaughtered_quantity['total_slaughtered']
                if remaining_breed_supply < 0:
                    raise ValueError(f"Cannot slaughter {slaughtered_quantity['total_slaughtered']} of breed {breed}. Insufficient breed supply.")
                total_dict[breed]['total_breed_supply'] = remaining_breed_supply

        # Convert the dictionary values to a list
        breeder_totals = list(total_dict.values())

        # Ensure all entries have 'breed' key
        for entry in breeder_totals:
            entry['breed'] = entry.get('breed', None)

        serializer = BreederTotalSerializer(breeder_totals, many=True)

        return Response(serializer.data)