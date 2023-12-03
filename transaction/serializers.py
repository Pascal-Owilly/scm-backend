# serializers.py
from rest_framework import serializers
from transaction.models import Abattoir, Breader, BreaderTrade, AbattoirPaymentToBreader

class AbattoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abattoir
        fields = '__all__'

class BreaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breader
        fields = '__all__'

class BreaderTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreaderTrade
        fields = '__all__'

class AbattoirPaymentToBreaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbattoirPaymentToBreader
        fields = '__all__'
