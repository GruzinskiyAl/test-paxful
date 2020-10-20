from django.db import models
from account.models import Wallet
from transaction.choices import TRANSACTION_STATUS_CHOICES


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='income_transactions')
    target_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='outcome_transactions')
    initial_amount = models.BigIntegerField()
    final_amount = models.BigIntegerField(null=True)
    status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS_CHOICES, default=0)

    @classmethod
    def get_transaction_commission_percent(cls, source_wallet, target_wallet):
        """
        Returns commission percent as float
        """
        if source_wallet.user == target_wallet.user:
            return 0.0
        return 0.015
