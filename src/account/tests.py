from django.test import TestCase
from account.models import *


class UserTestCase(TestCase):

    def test_username_setup(self):
        """Username setting up for new user"""
        user = User.objects.create(
            email='test@test.test',
            password='password'
        )
        self.assertTrue(user.username)

    def test_user_wallet_creation(self):
        """Create wallet on users creation"""
        user = User.objects.create(
            email='test@test.test',
            password='password'
        )
        self.assertEqual(user.wallets.count(), 1)

        user.first_name = "test"
        user.save()
        self.assertEqual(user.wallets.count(), 1)


class WalletTestCase(TestCase):
    def test_wallet_creation_address(self):
        """Wallet address setting up"""
        user = User.objects.create(
            email='test@test.test',
            password='password'
        )
        wallet = user.wallets.last()
        address = wallet.address
        self.assertTrue(address)

        wallet.balance = 123
        wallet.save()
        wallet.refresh_from_db()
        self.assertEqual(address, wallet.address)