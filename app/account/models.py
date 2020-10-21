import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from bitcoin import privtopub, pubtoaddr, random_key


class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        created = not self.pk

        if not self.username:
            self.username = str(uuid.uuid4())

        super().save(*args, **kwargs)

        if created:
            self.wallets.create()


class Wallet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wallets')
    address = models.CharField(max_length=128, primary_key=True, editable=False)
    public_key = models.CharField(max_length=130, editable=False)
    private_key = models.CharField(max_length=128, default=random_key, editable=False)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.user.email}__{self.pk}'

    def save(self, *args, **kwargs):
        created = not self.pk

        if created:
            self.public_key = privtopub(self.private_key)
            self.address = pubtoaddr(self.public_key)

        super().save(*args, **kwargs)
