from django.shortcuts import render
from slaughter_house.models import SlaughterhouseRecord
from rest_framework import viewsets
from django.db.models import Sum
from django.http import JsonResponse

from slaughter_house.serializers import SlaughterhouseRecordSerializer
from transaction.models import BreaderTrade
import logging

logger = logging.getLogger(__name__)


class SlaughterhouseRecordViewSet(viewsets.ModelViewSet):

    queryset = SlaughterhouseRecord.objects.all()
    serializer_class = SlaughterhouseRecordSerializer

def supply_vs_demand_statistics(request):
    # Get total bred quantities per breed
    bred_quantities = BreaderTrade.objects.values('breed').annotate(total_bred=Sum('breeds_supplied'))

    # Get total slaughtered quantities per breed
    slaughtered_quantities = SlaughterhouseRecord.objects.values('breed').annotate(total_slaughtered=Sum('quantity'))

    # Combine the data for supply vs demand comparison
    supply_vs_demand_data = []

    for bred_quantity in bred_quantities:
        breed = bred_quantity['breed']
        total_bred = bred_quantity['total_bred']

        slaughtered_quantity = next(
            (item['total_slaughtered'] for item in slaughtered_quantities if item['breed'] == breed),
            0
        )

        if slaughtered_quantity > total_bred:
            # Log the error
            logger.error(f"Breed: {breed}, Slaughtered Quantity: {slaughtered_quantity}, Total Breed Supply: {total_bred}")
            logger.error(f"Remaining Breed Supply after slaughter: {total_bred - slaughtered_quantity}")

        supply_vs_demand_data.append({
            'breed': breed,
            'total_bred': total_bred,
            'total_slaughtered': slaughtered_quantity,
        })

    return JsonResponse({'supply_vs_demand_data': supply_vs_demand_data})