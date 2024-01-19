from rest_framework import serializers
from .models import Invoice, Buyer,LetterOfCredit
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


class LetterOfCreditSerializer(serializers.ModelSerializer):
    buyer = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = LetterOfCredit
        fields = ['id', 'buyer', 'status', 'lc_document', 'issue_date']

    def get_buyer(self, obj):
        return str(obj.buyer) if obj.buyer else None