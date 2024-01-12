# serializers.py
from rest_framework import serializers
from .models import CustomUser, UserProfile, Payment, CustomerService
from rest_framework_simplejwt.tokens import RefreshToken
from transaction.serializers import BreaderTradeSerializer
from transaction.models import BreaderTrade
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RoleSerializer(serializers.Serializer):
    roleChoices = serializers.ListField()

    def to_representation(self, instance):
        return {'roleChoices': instance}
         
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate_password(self, value):
        try:
            # Use Django's built-in password validation
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password', None)  # Remove confirm_password from validated_data

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        groups_data = validated_data.pop('groups', [])

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        user.groups.set(groups_data)

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['access_token'] = str(RefreshToken.for_user(instance).access_token)
        representation['refresh_token'] = str(RefreshToken.for_user(instance))
        return representation

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

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

class CustomerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerService
        fields = '__all__'

