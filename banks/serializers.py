from rest_framework import serializers
from .models import Status, Bank, BankBranch, Payment, BankUser, Financier, FinancierUser


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class BankBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankBranch
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class BankUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankUser
        fields = '__all__'


class FinancierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financier
        fields = '__all__'


class FinancierUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancierUser
        fields = '__all__'
