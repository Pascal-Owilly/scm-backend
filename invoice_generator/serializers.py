from rest_framework import serializers
from .models import Invoice, Buyer,LetterOfCredit, LetterOfCreditSellerToTrader, PurchaseOrder, ProformaInvoiceFromTraderToSeller, Quotation
from custom_registration.models import CustomUser  
from logistics.serializers import LogisticsStatusSerializer, LogisticsStatus


# Local Buyers and sellers

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class LetterOfCreditSellerToTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetterOfCreditSellerToTrader
        fields = '__all__'

class ProformaInvoiceFromTraderToSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProformaInvoiceFromTraderToSeller
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'buyer', 'full_name']  # Include other fields as needed

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

# Buyer and quotatuin

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'

