from django.db import models
from authentications.models import User


class Wallet(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    user = models.ForeignKey(User)
    wallet_id = models.CharField(max_length=30)
    token_wallet = models.CharField(max_length=30)
