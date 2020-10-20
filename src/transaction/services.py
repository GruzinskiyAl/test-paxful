from django.db import transaction
from django.shortcuts import get_object_or_404

from account.models import Wallet
from transaction.models import Transaction
from transaction import choices


def execute_wallet_transaction(transaction_data):
    """
    Atomic saving transaction between wallets
    """

    with transaction.atomic():
        breakpoint()
        source_wallet = transaction_data.get('source_wallet')
        target_wallet = transaction_data.get('target_wallet')

        initial_amount = transaction_data.get('initial_amount')
        if source_wallet.balance >= initial_amount:
            transaction_data['status'] = choices.TRANSACTION_SUCCESS_STATUS
            percent_value = Transaction.get_transaction_commission_percent(source_wallet, target_wallet)
            final_amount = int(initial_amount * (1 - percent_value))
            transaction_data['final_amount'] = final_amount

            source_wallet.balance = source_wallet.balance - initial_amount
            target_wallet.balance = target_wallet.balance + final_amount
            source_wallet.save(update_fields=('balance', ))
            target_wallet.save(update_fields=('balance', ))

        return Transaction.objects.create(**transaction_data)
