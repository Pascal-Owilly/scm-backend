# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Abattoir, Breader, BreaderTrade, AbattoirPayment
from .serializers import AbattoirSerializer, BreaderSerializer, BreaderTradeSerializer, AbattoirPaymentSerializer
import logging

class AbattoirViewSet(viewsets.ModelViewSet):
    queryset = Abattoir.objects.all()
    serializer_class = AbattoirSerializer

class BreaderViewSet(viewsets.ModelViewSet):
    queryset = Breader.objects.all()
    serializer_class = BreaderSerializer

logger = logging.getLogger(__name__)

class BreaderTradeViewSet(viewsets.ModelViewSet):
    queryset = BreaderTrade.objects.all()
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


class AbattoirPaymentViewSet(viewsets.ModelViewSet):
    queryset = AbattoirPayment.objects.all()
    serializer_class = AbattoirPaymentSerializer
