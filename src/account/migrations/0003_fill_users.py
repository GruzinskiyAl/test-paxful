import random
from bitcoin import privtopub, pubtoaddr, random_key
from django.db import migrations

USERS = [
    {
        "username": "user+1@mail.com",
        "email": "user+1@mail.com",
        "first_name": "User1",
        "last_name": "User1",
        "password": "user1"
    },
    {
        "username": "user+2@mail.com",
        "email": "user+2@mail.com",
        "first_name": "User2",
        "last_name": "User2",
        "password": "user2"
    },
    {
        "username": "user+3@mail.com",
        "email": "user+3@mail.com",
        "first_name": "User3",
        "last_name": "User3",
        "password": "user3"
    },
    {
        "username": "user+4@mail.com",
        "email": "user+4@mail.com",
        "first_name": "User4",
        "last_name": "User4",
        "password": "user4"
    },
    {
        "username": "user+5@mail.com",
        "email": "user+5@mail.com",
        "first_name": "User5",
        "last_name": "User5",
        "password": "user5"
    },
    {
        "username": "user+6@mail.com",
        "email": "user+6@mail.com",
        "first_name": "User6",
        "last_name": "User6",
        "password": "user6"
    }
]


def forwards(apps, schema_editor):
    User = apps.get_model('account', 'User')
    users = [User(**data) for data in USERS]
    users_queryset = User.objects.bulk_create(users)
    for user in users_queryset:
        private_key = random_key()
        public_key = privtopub(private_key)
        address = pubtoaddr(public_key)
        balance = random.randint(1,100)
        user.wallets.create(private_key=private_key, public_key=public_key, address=address, balance=balance)


def backwards(apps, schema_editor):
    User = apps.get_model('account', 'User')
    User.objects.exclude(is_staff=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_wallet'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
