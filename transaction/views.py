from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Abattoir, Breader, BreaderTrade, AbattoirPaymentToBreader
from .serializers import AbattoirSerializer, BreaderSerializer, BreaderTradeSerializer, AbattoirPaymentToBreaderSerializer
import logging
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Sum




class AbattoirViewSet(viewsets.ModelViewSet):
    queryset = Abattoir.objects.all()
    serializer_class = AbattoirSerializer

class BreaderViewSet(viewsets.ModelViewSet):
    queryset = Breader.objects.all()
    serializer_class = BreaderSerializer

logger = logging.getLogger(__name__)

class BreaderTradeViewSet(viewsets.ModelViewSet):

    queryset = BreaderTrade.objects.all().order_by('-transaction_date')
    serializer_class = BreaderTradeSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            # Log the exception
            logger.error(f"Error in creating BreaderTrade: {str(e)}")
            # Print the error to the console during development
            print(f"Error in creating BreaderTrade: {str(e)}")
            # Return a response indicating the error
            return Response({"error": "An error occurred while creating BreaderTrade."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def breader_info(self, request, pk=None):
        """
        Retrieve detailed information about a specific BreaderTrade.

        Example URL: /api/breader-trade/{pk}/breader-info/
        """
        try:
            breader_trade = self.get_object()
            breader_data = BreaderSerializer(breader_trade.breader).data
            return Response(breader_data)
        except Exception as e:
            # Log the exception
            logger.error(f"Error in retrieving Breader information: {str(e)}")
            # Print the error to the console during development
            print(f"Error in retrieving Breader information: {str(e)}")
            # Return a response indicating the error
            return Response({"error": "An error occurred while retrieving Breader information."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def total_quantity(self, request):
        total_quantity_by_breed = BreaderTrade.objects.values('breed').annotate(total_quantity=Sum('breads_supplied'))
        return Response({'total_quantity_by_breed': total_quantity_by_breed})
        print(total_quantity_by_breed)

class BreaderCountView(APIView):
    def get(self, request, format=None):
        breader_count = Breader.objects.count()
        return Response({'breader_count': breader_count}, status=status.HTTP_200_OK)

class AbattoirPaymentToBreaderViewSet(viewsets.ModelViewSet):
    queryset = AbattoirPaymentToBreader.objects.all()
    serializer_class = AbattoirPaymentToBreaderSerializer

