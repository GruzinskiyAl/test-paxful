import random
from bitcoin import privtopub, pubtoaddr, random_key
from django.db import migrations


def forwards(apps, schema_editor):
    User = apps.get_model('account', 'User')
    users = [
        User(
            email=f'user{i}@mail.com',
            username=f'user{i}@mail.com',
            first_name=f'user{i}',
            last_name=f'user{i}',
            password=f'user{i}',
        ) for i in range(1, 6)
    ]
    users_queryset = User.objects.bulk_create(users)
    for user in users_queryset:
        private_key = random_key()
        public_key = privtopub(private_key)
        address = pubtoaddr(public_key)
        balance = random.randint(1, 100)
        user.wallets.create(private_key=private_key, public_key=public_key, address=address, balance=balance)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_wallet'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
