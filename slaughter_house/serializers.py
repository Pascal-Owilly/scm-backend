from rest_framework import serializers
from slaughter_house.models import SlaughterhouseRecord

class SlaughterhouseRecordSerializer(serializers.ModelSerializer):
    quantity_left = serializers.ReadOnlyField()  # Add this line to include quantity_left

    class Meta:
        model = SlaughterhouseRecord
        fields = '__all__'

class ComparisonResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    reference = serializers.CharField()
    breed = serializers.CharField()
    trade_weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cut_weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight_loss_percentage = serializers.FloatField()
    classification = serializers.CharField()