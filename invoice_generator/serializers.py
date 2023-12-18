from rest_framework import serializers
from .models import Invoice, Buyer

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer()

    class Meta:
        model = Invoice
        fields = '__all__'

    # Add additional fields for UI-related data
    # flash_message = serializers.CharField(allow_blank=True, required=False)
    # notifications = serializers.CharField(allow_blank=True, required=False)
    # purchase_issuance = serializers.BooleanField(required=False)
    # banking_transactions = serializers.BooleanField(required=False)
    # cataloging_live_deals = serializers.BooleanField(required=False)
    # management_of_deals = serializers.BooleanField(required=False)
    # tracking_financed_paid_off_deals = serializers.BooleanField(required=False)

    # def create(self, validated_data):
    #     buyer_data = validated_data.pop('buyer')
    #     buyer_instance = Buyer.objects.create(**buyer_data)
    #     validated_data['buyer'] = buyer_instance
    #     return super().create(validated_data)
