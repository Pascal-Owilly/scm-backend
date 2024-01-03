# serializers.py
from rest_framework import serializers
from .models import CustomUser, UserProfile, Payment  
from rest_framework_simplejwt.tokens import RefreshToken
from transaction.serializers import BreaderTradeSerializer
from transaction.models import BreaderTrade
class RoleSerializer(serializers.Serializer):
    roleChoices = serializers.ListField()

    def to_representation(self, instance):
        return {'roleChoices': instance}
         
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        from custom_registration.serializers import CustomUserSerializer
        password = validated_data.pop('password')
        groups_data = validated_data.pop('groups', [])  # Get groups data, default to an empty list
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        # Save user first, then set user groups
        user.groups.set(groups_data)

        # Return the user instance instead of a dictionary
        return user

    def to_representation(self, instance):
        # Override to_representation to include additional fields in the serialized data
        representation = super().to_representation(instance)
        representation['access_token'] = str(RefreshToken.for_user(instance).access_token)
        representation['refresh_token'] = str(RefreshToken.for_user(instance))
        return representation

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'profile_pic']  # Include other fields


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    My custom serializer for TokenObtainPairView.
    Includes any additional fields needed in the token payload.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()

    def validate(self, attrs):
        # Your validation logic here (if needed)
        return attrs

class LogoutSerializer(serializers.Serializer):
    """
    Serializer for handling the logout response.
    """
    detail = serializers.CharField(default="Logout successful.")

# payment

# serializers.py

class PaymentSerializer(serializers.ModelSerializer):
    breeder_trade = BreaderTradeSerializer()

    class Meta:
        model = Payment
        fields = ['status', 'breeder_trade', 'payment_code', 'payment_initiation_date']

    def create(self, validated_data):
        breeder_trade_data = validated_data.pop('breeder_trade')
        breeder_trade_instance = BreaderTrade.objects.create(**breeder_trade_data)
        payment_instance = Payment.objects.create(breeder_trade=breeder_trade_instance, **validated_data)
        return payment_instance


