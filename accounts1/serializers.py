from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Profile

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['profile_pic']:
            data['profile_pic'] = '/media/default.png'  # Use the path to your default image
        return data

    def validate_bio(self, value):
        # Add custom validation for the "bio" field here
        # For example, ensure the bio is not too long or meets specific criteria
        if len(value) > 500:
            raise serializers.ValidationError("Bio is too long.")
        return value

    def validate_current_city(self, value):
        # Add custom validation for the "current_city" field here
        # For example, ensure the current_city meets specific criteria
        if len(value) > 50:
            raise serializers.ValidationError("Current city is too long.")
        return value
