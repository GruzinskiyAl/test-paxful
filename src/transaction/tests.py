from django.test import TestCase
from account.models import *
from transaction.services import execute_wallet_transaction
from transaction.choices import TRANSACTION_SUCCESS_STATUS, TRANSACTION_FAIL_STATUS


class TransactionTestCase(TestCase):
    def setUp(self):
        self.source_user = User.objects.create(email="source@test.test", password="password")
        self.target_user = User.objects.create(email="target@test.test", password="password")
        self.source_user.wallets.all().update(balance=1000)

    def test_success_transaction(self):
        """Transaction between wallets"""
        source_wallet = self.source_user.wallets.last()
        target_wallet = self.target_user.wallets.last()

        source_balance_init = source_wallet.balance
        target_balance_init = target_wallet.balance

        data = {
            'initial_amount': 20,
            'source_wallet': source_wallet,
            'target_wallet': target_wallet,
        }
        execute_wallet_transaction(data)

        source_wallet.refresh_from_db()
        target_wallet.refresh_from_db()

        self.assertTrue(source_balance_init > source_wallet.balance)
        self.assertTrue(target_balance_init < target_wallet.balance)

        self.assertEqual(source_wallet.outcome_transactions.last().status, TRANSACTION_SUCCESS_STATUS)

    def test_fail_transaction(self):
        """Transaction between wallets fail if initial amount bigger then source balance"""
        source_wallet = self.source_user.wallets.last()
        target_wallet = self.target_user.wallets.last()

        source_balance_init = source_wallet.balance
        target_balance_init = target_wallet.balance

        data = {
            'initial_amount': 1100,
            'source_wallet': source_wallet,
            'target_wallet': target_wallet,
        }
        execute_wallet_transaction(data)

        source_wallet.refresh_from_db()
        target_wallet.refresh_from_db()

        self.assertTrue(source_balance_init == source_wallet.balance)
        self.assertTrue(target_balance_init == target_wallet.balance)

        self.assertEqual(source_wallet.outcome_transactions.last().status, TRANSACTION_FAIL_STATUS)
