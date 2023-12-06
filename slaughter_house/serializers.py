from rest_framework import serializers
from slaughter_house.models import SlaughterhouseRecord

class SlaughterhouseRecordSerializer(serializers.ModelSerializer):
    quantity_left = serializers.ReadOnlyField()  # Add this line to include quantity_left

    class Meta:
        model = SlaughterhouseRecord
        fields = '__all__'