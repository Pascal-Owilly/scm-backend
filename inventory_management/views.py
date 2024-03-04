from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from .models import InventoryBreed, InventoryBreedSales, BreedCut
from .serializers import InventoryBreedSerializer, InventoryBreedSalesSerializer, BreedCutSerializer, BreederTotalSerializer, BreedCutTotalSerializer
from transaction.models import BreaderTrade
from slaughter_house.models import SlaughterhouseRecord
from django.db.models import Sum
from rest_framework.response import Response

from logistics.models import ControlCenter

class InventoryBreedViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreed.objects.all()
    serializer_class = InventoryBreedSerializer

class BreedCutViewSet(viewsets.ModelViewSet):
    queryset = BreedCut.objects.all()
    serializer_class = BreedCutSerializer

class BreedCutTotalViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            # Calculate total breed cut for each part_name
            breed_cut_totals = (
                BreedCut.objects
                .values('breed', 'part_name', 'quantity', 'sale_type', 'sale_date')
                .annotate(total_breed_cut=Sum('quantity'))
            )

            # Convert the queryset to a list
            cut_totals = list(breed_cut_totals)

            # Ensure all entries have 'part_name' key
            for entry in cut_totals:
                entry['part_name'] = entry.get('part_name', None)

            serializer = BreedCutTotalSerializer(cut_totals, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InventoryBreedSalesViewSet(viewsets.ModelViewSet):
    queryset = InventoryBreedSales.objects.all()
    serializer_class = InventoryBreedSalesSerializer

class BreederTotalViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            # Calculate total breed supply from BreaderTrade
            breeder_totals = (
                BreaderTrade.objects
                .values('control_center__id', 'breed')
                .annotate(total_breed_supply=Sum('breeds_supplied'))
            )

            # Calculate total slaughtered from SlaughterhouseRecord
            slaughtered_quantities = (
                SlaughterhouseRecord.objects
                .values('breed')
                .annotate(total_slaughtered=Sum('quantity'))
            )

            # Create a dictionary to hold the total breed supply per breed and control center
            total_dict = {}

            # Calculate total breed supply per control center and breed
            for total in breeder_totals:
                control_center_id = total['control_center__id']
                breed = total['breed']
                total_dict.setdefault((control_center_id, breed), {'breader__id': control_center_id, 'breed': breed, 'total_breed_supply': 0})
                total_dict[(control_center_id, breed)]['total_breed_supply'] += total['total_breed_supply']

            # Subtract slaughtered quantities from the total breed supply per control center and breed
            for slaughtered_quantity in slaughtered_quantities:
                breed = slaughtered_quantity['breed']
                for key, value in total_dict.items():
                    control_center_id, breed_in_dict = key
                    if breed_in_dict == breed:
                        total_dict[key]['total_breed_supply'] -= slaughtered_quantity['total_slaughtered']
                        # Ensure the total breed supply doesn't go negative
                        if total_dict[key]['total_breed_supply'] < 0:
                            total_dict[key]['total_breed_supply'] = 0  # Set to 0 if negative

            # Convert the dictionary values to a list
            breeder_totals = list(total_dict.values())

            serializer = BreederTotalSerializer(breeder_totals, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
