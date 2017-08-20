from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Shop(models.Model):
    user = models.OneToOneField(User, unique=True)
    shop_id = models.IntegerField()
    shop_mobile = models.CharField(max_length=45)
    shop_name = models.CharField(max_length=45)
    deposit = models.DecimalField(max_digits=15, decimal_places=5)
    bonus = models.DecimalField(max_digits=15, decimal_places=5)
    discount = models.DecimalField(max_digits=15, decimal_places=5)
    status = models.CharField(max_length=45)


class Broker(models.Model):
    user = models.OneToOneField(User, unique=True)
    shop_mobile = models.CharField(max_length=45)
    broker_mobile = models.CharField(max_length=45)
    broker_name = models.CharField(max_length=45)
    broker_email = models.CharField(max_length=45)
    status = models.CharField(max_length=45)

class Customer(models.Model):
    user = models.OneToOneField(User, unique=True)
    shop_mobile = models.CharField(max_length=45)
    broker_mobile = models.CharField(max_length=45)
    customer_mobile = models.CharField(max_length=45)
    status = models.CharField(max_length=45)


class Fee(models.Model):
    fee = models.FloatField()
