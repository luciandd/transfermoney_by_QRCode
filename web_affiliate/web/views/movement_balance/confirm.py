from authentications.utils import get_auth_header
from web_affiliate.utils import setup_logger
from web_affiliate import api_settings

from django.contrib import messages
from django.views.generic.base import View
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings

import logging
import time
import requests

logger = logging.getLogger(__name__)


class ConfirmPayment(View):
    logger = logger
    order_url = settings.HOST_NAMES + "payment/" + api_settings.API_VERSION + "/orders/{order_id}"

    def dispatch(self, request, *args, **kwargs):
        self.logger = setup_logger(request, logger)
        return super(ConfirmPayment, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.logger.info('========== Start confirm payment order to backend service ==========')
        if kwargs.get('order_id', None) is None:
            raise Exception("Order id is None")

        try:

            order_id = kwargs.get('order_id', None)
            url = self.order_url.format(order_id=order_id)

            self.logger.info('Confirm payment url is - {};'.format(url))
            headers = get_auth_header(self.request, self.request.user)

            start_date = time.time()
            response = requests.post(url, headers=headers, verify=settings.CERT)
            done = time.time()
            self.logger.info('Response time for confirm payment - {} sec.'.format(done - start_date))
            self.logger.info('Response data from backend is {}'.format(response.content))
            json_data = response.json()
            status = json_data.get('status', {})

            if status.get('code', '') == "success":
                self.logger.info('========== End confirm payment order to backend service ==========')
                return redirect('web:history')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    json_data.get('message', {})
                )
                return redirect('web:history')
        except:
            pass

        return HttpResponseBadRequest()
