from rest_framework import serializers
from .models import Invoice, Buyer, PurchaseOrder, Item, Product
from custom_registration.models import CustomUser  
from logistics.serializers import LogisticsStatusSerializer

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    # logistics_status = LogisticsStatusSerializer()  # Update this line

    buyer = BuyerSerializer(required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

        def create(self, validated_data):
            buyer_data = validated_data.pop('buyer', None)

            if buyer_data:
                user_data = buyer_data.pop('user', None)

                # Ensure the user data is provided
                if user_data:
                    user, created = CustomUser.objects.get_or_create(**user_data)

                    # Additional fields can be set here if needed
                    # user.field_name = user_data['field_name']

                    validated_data['buyer'] = user

            return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'breed', 'part_name', 'sale_type', 'unit_price')

class ItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)  

    class Meta:
        model = Item
        fields = ('id', 'quantity', 'product')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # items = ItemSerializer()

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'purchase_order_date', 'purchase_order_number', 'status', 'vendor_notification', '_original_status', 'buyer', 'items')
