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
                .values('breeder__id', 'breed')
                .annotate(total_breed_supply=Sum('breeds_supplied'))
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
                breeder_id = total['breeder__id']
                breed = total['breed']
                total_dict.setdefault(breed, {'breeder__id': breeder_id, 'total_breed_supply': 0, 'breed': breed})
                total_dict[breed]['total_breed_supply'] += total['total_breed_supply']

            for slaughtered_quantity in slaughtered_quantities:
                breed = slaughtered_quantity['breed']
                total_dict.setdefault(breed, {'breeder__id': None, 'total_breed_supply': 0, 'breed': breed})
                
                print(f"Breed: {breed}, Slaughtered Quantity: {slaughtered_quantity['total_slaughtered']}, Total Breed Supply: {total_dict[breed]['total_breed_supply']}")
                
                # Check if breed exists in breeder_totals before subtracting
                # if breed in total_dict:
                #     # Validate before subtracting
                #     remaining_breed_supply = total_dict[breed]['total_breed_supply'] - slaughtered_quantity['total_slaughtered']
                #     print(f"Remaining Breed Supply after slaughter: {remaining_breed_supply}")
                    
                #     if remaining_breed_supply < 0:
                #         raise ValidationError(f"Cannot slaughter {slaughtered_quantity['total_slaughtered']} of breed {breed}. Insufficient breed supply.")
                    
                #     total_dict[breed]['total_breed_supply'] = remaining_breed_supply
                # else:
                #     raise ValidationError(f"Breed {breed} not found in breeder_totals.")

# Rest of your code...

            # Convert the dictionary values to a list
            breeder_totals = list(total_dict.values())

            # Ensure all entries have 'breed' key
            for entry in breeder_totals:
                entry['breed'] = entry.get('breed', None)

            serializer = BreederTotalSerializer(breeder_totals, many=True)

            return Response(serializer.data)

        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
