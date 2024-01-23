from rest_framework import serializers
from .models import Invoice, Buyer,LetterOfCredit
from custom_registration.models import CustomUser  
from logistics.serializers import LogisticsStatusSerializer, LogisticsStatus


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer(required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        buyer_data = validated_data.pop('buyer', None)

        if buyer_data:
            buyer = buyer_data.pop('buyer', None)

            if buyer_data:
                buyer, created = Buyer.objects.get_or_create(**buyer_data)
                validated_data['buyer'] = buyer

        return super().create(validated_data)

class LetterOfCreditSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer(allow_null=True,required=False)
    invoice_number = serializers.SerializerMethodField()

    class Meta:
        model = LetterOfCredit
        fields = ['id', 'status', 'buyer', 'lc_document', 'issue_date', 'invoice_number']

    def get_buyer(self, obj):
        return str(obj.buyer) if obj.buyer else None

    def get_invoice_number(self, obj):
        if hasattr(obj, 'invoice') and obj.invoice:
            return obj.invoice.invoice_number
        return None

class LogisticsStatusSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()  # Include the InvoiceSerializer here

    class Meta:
        model = LogisticsStatus
        fields = ['id', 'status', 'timestamp', 'invoice']
