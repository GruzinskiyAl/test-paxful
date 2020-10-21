from django.db import models

from account.models import Wallet
from transaction.choices import TRANSACTION_STATUS_CHOICES


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='outcome_transactions')
    target_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='income_transactions')
    initial_amount = models.BigIntegerField()
    final_amount = models.BigIntegerField(null=True)
    status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS_CHOICES)
