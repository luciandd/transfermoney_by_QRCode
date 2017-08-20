from django.db import models


class Transaction(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    shop_id = models.CharField(max_length=45, default=None)
    broker_id = models.CharField(max_length=45, default=None)
    customer_id = models.CharField(max_length=45, default=None)
    amount = models.IntegerField()
    status = models.CharField(max_length=10)
    transaction_time = models.DateTimeField(default=None)
