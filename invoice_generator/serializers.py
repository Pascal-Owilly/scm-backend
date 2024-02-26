from rest_framework import serializers
from .models import Invoice, Buyer,LetterOfCredit, LetterOfCreditSellerToTrader, PurchaseOrder, ProformaInvoiceFromTraderToSeller, Quotation, DocumentToSeller
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
    full_name = serializers.CharField(source='get_full_name')
    username = serializers.CharField(source='get_user_name')
    email = serializers.CharField(source='get_user_email')
    address = serializers.CharField(source='get_user_address')
    country = serializers.CharField(source='get_user_country')

    class Meta:
        model = Buyer
        fields = ['id', 'buyer', 'created_at', 'full_name', 'username', 'email', 'address', 'country']


class InvoiceSerializer(serializers.ModelSerializer):
    buyer_full_name = serializers.SerializerMethodField()
    buyer_user_name = serializers.SerializerMethodField()
    buyer_user_email = serializers.SerializerMethodField()
    buyer_user_country = serializers.SerializerMethodField()
    buyer_user_address = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def get_buyer_full_name(self, obj):
        if obj.buyer:
            return obj.buyer.get_full_name()
        return "Unknown"

    def get_buyer_user_name(self, obj):
        if obj.buyer:
            return obj.buyer.get_user_name()
        return "Unknown"

    def get_buyer_user_email(self, obj):
        if obj.buyer:
            return obj.buyer.get_user_email()
        return "Unknown"

    def get_buyer_user_country(self, obj):
        if obj.buyer:
            return obj.buyer.get_user_country()
        return "Unknown"

    def get_buyer_user_address(self, obj):
        if obj.buyer:
            return obj.buyer.get_user_address()
        return "Unknown"

class DocumentToSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentToSeller
        fields = ['id', 'seller', 'message', 'uploaded_at']


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
        fields = ['id', 'seller', 'buyer', 'product', 'confirm', 'quantity', 'delivery_time', 'unit_price', 'message', 'created_at']

