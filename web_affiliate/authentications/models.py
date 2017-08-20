from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Authentications(models.Model):
    user = models.OneToOneField(User, unique=True)
    access_token = models.CharField(max_length=256)
    last_updated = models.DateTimeField(null=True, blank=True)
    correlation_id = models.CharField(max_length=128, default='')


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    # role = models.IntegerField()
    # mobile = models.CharField(max_length=45)
    permissions = models.CharField(max_length=45)
    address = models.CharField(max_length=130)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()
