# serializers.py
from rest_framework import serializers
from .models import CustomUser, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'id_number', 'market', 'community', 'head_of_family', 'country', 'groups', 'password')

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
