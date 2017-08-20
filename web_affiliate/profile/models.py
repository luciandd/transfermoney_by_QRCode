from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    id_auth_user = models.IntegerField()
    role = models.IntegerField()
    status = models.IntegerField()
    email = models.CharField(max_length=45)
    mobile_phone = models.CharField(max_length=45)

