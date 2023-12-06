from rest_framework import serializers
from slaughter_house.models import SlaughterhouseRecord

class SlaughterhouseRecordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SlaughterhouseRecord
        fields = '__all__'