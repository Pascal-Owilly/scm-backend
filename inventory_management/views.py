from inventory_management.models import Inventory
from rest_framework import serializers, viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action  # Import the action decorator for search
from inventory_management.serializers import InventorySerializer
from django.db.models import Q
from rest_framework.response import Response

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().order_by('-stock_date')
    serializer_class = InventorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name__icontains']
    
    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.query_params.get('query', '')

        # Perform a search across multiple fields and models using Q objects
        results = Inventory.objects.filter(
            Q(name__icontains=query)
        ).order_by('-stock_date')

        serializer = InventorySerializer(results, many=True)
        return Response(serializer.data)