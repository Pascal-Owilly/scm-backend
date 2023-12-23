from rest_framework import serializers
from .models import Invoice, Buyer
from custom_registration.models import CustomUser  

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
                user_data = buyer_data.pop('user', None)

                # Ensure the user data is provided
                if user_data:
                    user, created = CustomUser.objects.get_or_create(**user_data)

                    # Additional fields can be set here if needed
                    # user.field_name = user_data['field_name']

                    validated_data['buyer'] = user

            return super().create(validated_data)

