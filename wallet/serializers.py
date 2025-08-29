from rest_framework import serializers
from decimal import Decimal
from .models import Wallet, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'description', 'created_at']
        read_only_fields = fields

class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'transactions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'balance', 'transactions', 'created_at', 'updated_at']

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value: Decimal):
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
