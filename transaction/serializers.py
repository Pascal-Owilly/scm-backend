# serializers.py
from rest_framework import serializers
from transaction.models import Abattoir, Breader, BreaderTrade, AbattoirPaymentToBreader
from custom_registration.models import CustomUser

class AbattoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abattoir
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['community', 'market', 'first_name', 'last_name']

class BreaderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Breader
        fields = '__all__'

class BreaderTradeSerializer(serializers.ModelSerializer):
    breeder_market = serializers.CharField(source='breeder.market', read_only=True)
    breeder_community = serializers.CharField(source='breeder.community', read_only=True)
    breeder_head_of_family = serializers.CharField(source='breeder.head_of_family', read_only=True)

    breeder_first_name = serializers.CharField(source='breeder.first_name', read_only=True)
    breeder_last_name = serializers.CharField(source='breeder.last_name', read_only=True)

    class Meta:
        model = BreaderTrade
        fields = '__all__'

class AbattoirPaymentToBreaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbattoirPaymentToBreader
        fields = '__all__'

    def create(self, validated_data):
        # Extract the 'breeder_trade' instance from the validated data
        breeder_trade_instance = validated_data.pop('breeder_trade')

        # Set the 'breeder_trade' field with the BreaderTrade instance
        validated_data['breeder_trade'] = breeder_trade_instance

        # Call the superclass create method with the modified data
        instance = super().create(validated_data)

        print("Created Instance ID:", instance.payments_id)

        return instance

