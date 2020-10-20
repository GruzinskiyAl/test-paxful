from django.db import transaction

from transaction.models import Transaction
from transaction import choices


@transaction.atomic
def execute_wallet_transaction(transaction_data):
    """
    Atomic saving transaction between wallets
    :param transaction_data: {
        initial_amount: int
        source_wallet: Wallet instance
        target_wallet: Wallet instance
    }
    :return: Transaction instance
    """
    source_wallet = transaction_data.get('source_wallet')
    target_wallet = transaction_data.get('target_wallet')

    initial_amount = transaction_data.get('initial_amount')
    if source_wallet.balance >= initial_amount:
        transaction_data['status'] = choices.TRANSACTION_SUCCESS_STATUS
        percent_value = Transaction.get_transaction_commission_percent()
        final_amount = int(initial_amount * (1 - percent_value))
        transaction_data['final_amount'] = final_amount

        source_wallet.balance = source_wallet.balance - initial_amount
        target_wallet.balance = target_wallet.balance + final_amount
        source_wallet.save(update_fields=('balance', ))
        target_wallet.save(update_fields=('balance', ))

    return Transaction.objects.create(**transaction_data)
