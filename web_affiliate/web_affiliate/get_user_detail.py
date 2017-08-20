from django.conf import settings
from authentications.apps import InvalidAccessToken
from authentications.models import Authentications

import logging

logger = logging.getLogger(__name__)


class GetUserDetailMixin(object):
    def _get_headers(self):
        if getattr(self, '_headers', None) is None:
            self._headers = self._get_auth_header(self.request.user)
        return self._headers

    def _get_auth_header(self, user):
        client_id = settings.CLIENTID
        client_secret = settings.CLIENTSECRET
        auth = Authentications.objects.get(user=user)
        access_token = auth.access_token
        correlation_id = auth.correlation_id

        headers = {
            'content-type': 'application/json',
            'correlation-id': correlation_id,
            'client_id': client_id,
            'client_secret': client_secret,
            'Authorization': 'Bearer {}'.format(access_token),
        }
        return headers

    def _get_correlaion_id(self):
        if getattr(self, '_correlation_id', None) is None:
            auth = Authentications.objects.get(user=self.request.user)
            self._correlation_id = auth.correlation_id
        return self._correlation_id
