from authentications.models import Authentications
from web_affiliate.utils import setup_logger
from web_affiliate import api_settings
import logging

import requests
from django.conf import settings
from authentications.utils import get_auth_header
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)


class HistoryListView(LoginRequiredMixin, TemplateView):
    template_name = "history/history.html"
    login_url = 'authentications:login'
    redirect_field_name = 'next'
    logger = logger
    order_url = settings.HOST_NAMES + "payment/" + api_settings.API_VERSION + "/orders"

    def dispatch(self, request, *args, **kwargs):
        self.logger = setup_logger(self.request, logger)
        return super(HistoryListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.logger.info('========== Start get order history list ==========')
        headers = get_auth_header(self.request, self.request.user)
        url = self.order_url
        response = requests.get(url=url, headers=headers, verify=settings.CERT)
        json_data = response.json()
        data = json_data.get('data')
        self.logger.info("Status of response history is {}".format(response.status_code))
        self.logger.info("Request url for get order history is {}".format(url))
        self.logger.info("Response for get order histories are {}".format(len(response.content)))

        if response.status_code == 200 and json_data.get('status', {}).get('code', '') == "success":
            user_id, user_type = self._get_user_id(self.request.user)
            result = {'data': data, 'user_id': int(user_id), 'user_type': user_type}
            self.logger.info('========== End get order history list ==========')
            return result
        else:
            if json_data.get('status', {}).get('code', '') == "access_token_expire":
                # TODO: redirect to login page
                logger.info('========== End get order history list ==========')
                raise Exception(response.content)

        raise Exception(response.content)

    def _get_user_id(self, user):
        user = Authentications.objects.get(user=user)
        correlation_id = user.correlation_id
        data = correlation_id.split("-")
        user_id = data[1]
        user_type = data[0]
        return user_id, user_type
