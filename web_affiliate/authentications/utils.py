from django.conf import settings
from authentications.models import Authentications, Profile

from django import template
import logging
register = template.Library()
logger = logging.getLogger(__name__)


def check_permissions_by_user(user, permission):
    try:
        authens = Profile.objects.get(user=user)
        permissions = authens.permissions
        if permission in permissions:
            return True
        else:
            return False
    except Exception as ex:
        return False


def get_auth_header(request, user):
    client_id = settings.CLIENTID
    client_secret = settings.CLIENTSECRET
    auth = Authentications.objects.get(user=user)
    access_token = auth.access_token
    client_ip = request.META['REMOTE_ADDR']

    headers = {
        'content-type': 'application/json',
        'client_id': client_id,
        'client_secret': client_secret,
        'Authorization': 'Bearer {}'.format(access_token),
        "X-IP-ADDRESS": client_ip
    }
    return headers
