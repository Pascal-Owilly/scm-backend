from django.shortcuts import render
from slaughter_house.models import SlaughterhouseRecord
from rest_framework import viewsets
from django.db.models import Sum
from django.http import JsonResponse

from slaughter_house.serializers import SlaughterhouseRecordSerializer
from inventory_management.models import BreedCut
from transaction.models import BreaderTrade
import logging
from django.views.decorators.csrf import csrf_exempt
from .serializers import ComparisonResultSerializer
logger = logging.getLogger(__name__)


class SlaughterhouseRecordViewSet(viewsets.ModelViewSet):

    queryset = SlaughterhouseRecord.objects.all().order_by('-slaughter_date')
    serializer_class = SlaughterhouseRecordSerializer

@csrf_exempt
def compare_weight_loss(request):
    if request.method == 'GET':
        # Retrieve all BreaderTrade records
        breader_trades = BreaderTrade.objects.all()
        
        # Retrieve all BreedCut records
        breed_cuts = BreedCut.objects.all()
        
        # Perform comparison logic
        comparison_results = []

        for trade in breader_trades:
            breed = trade.breed
            trade_weight = trade.goat_weight
            total_cut_weight = 0
            
            # Calculate the total weight cut for the breed
            for cut in breed_cuts.filter(breed=breed):
                if cut.weight:  # Check if weight is not None or empty
                    total_cut_weight += cut.quantity * int(cut.weight)

            # Calculate the weight loss percentage
            if trade_weight > 0:  # Check if trade_weight is not 0 to avoid division by zero
                weight_loss_percentage = ((trade_weight - total_cut_weight) / trade_weight) * 100
            else:
                weight_loss_percentage = 0

            # Classify weight loss
            if weight_loss_percentage < 5:
                classification = 'Normal'
            elif weight_loss_percentage < 10:
                classification = 'A little more'
            else:
                classification = 'Too much'

            # Create comparison result object
            comparison_result = {
                'id': trade.id,
                'reference': trade.reference,
                'breed': breed,
                'trade_weight': trade_weight,
                'total_cut_weight': total_cut_weight,
                'weight_loss_percentage': weight_loss_percentage,
                'classification': classification
            }

            # Serialize the comparison result
            serializer = ComparisonResultSerializer(data=comparison_result)
            serializer.is_valid()
            comparison_results.append(serializer.data)

        return JsonResponse(comparison_results, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are supported for this endpoint'}, status=405)

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