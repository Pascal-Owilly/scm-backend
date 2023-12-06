from django.shortcuts import render
from slaughter_house.models import SlaughterhouseRecord
from rest_framework import viewsets
from slaughter_house.serializers import SlaughterhouseRecordSerializer

class SlaughterhouseRecordViewSet(viewsets.ModelViewSet):

    queryset = SlaughterhouseRecord.objects.all()
    serializer_class = SlaughterhouseRecordSerializer

