from rest_framework import serializers
from transaction.models import Transaction
from transaction.services import execute_wallet_transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('initial_amount', 'source_wallet', 'target_wallet', 'final_amount', 'status')
        read_only_fields = ('final_amount', 'status')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['source_wallet'] == attrs['target_wallet']:
            raise serializers.ValidationError('Cannot create transaction on the same wallet.')
        return attrs

    def create(self, validated_data):
        return execute_wallet_transaction(validated_data)
