from account.models import *


def test_user_creation():
    user = User.objects.create(
        email='test@test.test',
        password='password'
    )
    assert user.username

