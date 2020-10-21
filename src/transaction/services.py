from django.db import transaction
from django.db.models import F

from account.models import Wallet
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
    source_wallet = Wallet.objects.select_for_update().get(pk=transaction_data.get('source_wallet').pk)
    target_wallet = Wallet.objects.select_for_update().get(pk=transaction_data.get('target_wallet').pk)

    initial_amount = transaction_data.get('initial_amount')
    if source_wallet.balance >= initial_amount:
        transaction_data['status'] = choices.TRANSACTION_SUCCESS_STATUS
        percent_value = Transaction.get_transaction_commission_percent()
        final_amount = int(initial_amount * (1 - percent_value))
        transaction_data['final_amount'] = final_amount

        Wallet.objects.filter(pk=source_wallet.pk).update(balance=F('balance') - initial_amount)
        Wallet.objects.filter(pk=target_wallet.pk).update(balance=F('balance') + final_amount)

    return Transaction.objects.create(**transaction_data)
