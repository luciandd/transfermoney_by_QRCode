from authentications.models import Authentications
from web_affiliate.utils import setup_logger

from django.conf import settings
from authentications.utils import get_auth_header
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from web_affiliate import api_settings

import logging
import requests
import time
import uuid

logger = logging.getLogger(__name__)


class BalanceMovementView(TemplateView):
    template_name = "movement_balance/details_page.html"
    _services_list = {}
    company_agent_id = "1"
    order_url = settings.HOST_NAMES + "payment/" + api_settings.API_VERSION + "/orders/{order_id}"
    cancel_order_url = settings.HOST_NAMES + "payment/" + api_settings.API_VERSION + "/orders/{order_id}"
    logger = logger

    def dispatch(self, request, *args, **kwargs):
        self.logger = setup_logger(self.request, logger)
        return super(BalanceMovementView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.logger.info('========== Start display movement balance details page ==========')
        if kwargs.get('order_id', None) is None:
            raise Exception("Order id is None")

        order_id = kwargs.get('order_id', None)
        url = self.order_url.format(order_id=order_id)

        services = self._get_services_list()
        sofs = self._get_sof_types_list()

        self.logger.info('Confirm payment url is {}'.format(url))
        headers = get_auth_header(self.request, self.request.user)

        start_date = time.time()
        response = requests.get(url, headers=headers, verify=settings.CERT)
        done = time.time()
        self.logger.info('Response time for confirm payment - {} sec.'.format(done - start_date))
        self.logger.info('Response data from backend is {}'.format(response.content))
        json_data = response.json()
        status = json_data.get('status', {})
        context = {}

        if response.status_code == 200 and status.get('code', '') == "success":
            self.logger.info('========== End display movement balance details page ==========')
            context["order_details"] = json_data.get('data', {})
            context["services"] = services
            context["sofs"] = sofs
            return context
        else:
            raise Exception(response.content)

    def post(self, request, *args, **kwargs):
        self.logger.info('========== Start cancel movement balance from company agent to other agent ==========')
        service_id = request.POST.get('service_id')
        ext_transaction_id = str(uuid.uuid4())

        if kwargs.get('order_id', None) is None:
            raise Exception("Order id is None")
        order_id = kwargs.get('order_id')
        self.logger.info("Order id to cancel is {} and external transaction id is {}".format(order_id, ext_transaction_id))
        self.logger.info("service is - {}".format(self._services_list.get(service_id)))
        user = Authentications.objects.get(user=self.request.user)

        params = {
            "ext_transaction_id": ext_transaction_id,
            "payment_method": {
                "payment_method_name": "Normal payment",
                "payment_method_ref": user.access_token
            },
        }

        headers = get_auth_header(self.request, self.request.user)
        url = self.cancel_order_url.format(order_id=order_id)

        response = requests.delete(url=url, headers=headers, json=params, verify=settings.CERT)
        json_data = response.json()
        self.logger.info("Response status from backend {}".format(response.content))
        status = json_data.get('status', {})

        if response.status_code == 200 and status.get('code', '') == "success":
            self.logger.info('========== End cancel movement balance from company agent to other agent ==========')
            return redirect('web:history')
        else:
            raise Exception(response.content)

    def _get_service_objects(self, service_id):
        service_list = self._get_services_list()
        services = {}
        if len(service_list) > 0:
            service_obj = [item for item in service_list if str(item.get("service_id")) == service_id]
            services = service_obj[0]
        return services

    def _get_sof_objects(self, sof_id):
        sof_list = self._get_sof_types_list()
        sof = {}
        if len(sof_list) > 0:
            sof_obj = [item for item in sof_list if str(item.get("sof_type_id")) == sof_id]
            sof = sof_obj[0]
        return sof

    def _get_services_list(self):
        if getattr(self, '_services', None) is None:
            self.logger.info("Getting equator service list by {} user id".format(self.request.user.username))
            headers = get_auth_header(self.request, self.request.user)
            url = settings.HOST_NAMES + api_settings.SERVICE_LIST_URL

            self.logger.info("Getting equator service list from backend with {} url".format(url))
            response = requests.get(url, headers=headers, verify=settings.CERT)
            self.logger.info("Get equator service list response status is {}".format(response.status_code))
            self.logger.info("Get equator service list response data is {}".format(response.content))

            json_data = response.json()
            data = json_data.get('data')

            if response.status_code == 200 and json_data["status"]["code"] == 'success':
                self.logger.info('Service count: {}'.format(len(data)))
                self._services_list = data

            elif json_data["status"]["code"] == "access_token_expire":
                self.logger.info("{} for {} username".format(json_data["status"]["message"], self.request.user))
                raise Exception(str(response.content))
        return self._services_list

    def _get_sof_types_list(self):
        if getattr(self, '_sof_type', None) is None:
            url = settings.HOST_NAMES + api_settings.SOF_TYPES_URL
            self.logger.info("Get choices for table from url: {}".format(url))
            headers = get_auth_header(self.request, self.request.user)
            response = requests.get(url, headers=headers, verify=settings.CERT)
            self.logger.info("Get sof type list response data is {}".format(response.content))
            json_data = response.json()
            self.logger.info("Response status code: {}".format(response.status_code))
            self._sof_type = json_data['data']
        return self._sof_type

    def _get_agent_sof_id(self, agent_id, currency):
        headers = get_auth_header(self.request, self.request.user)
        url = settings.HOST_NAMES + api_settings.GET_AGENT_SOF_ID_URL.format(agentId=agent_id, currency=currency)

        self.logger.info("URL for get agent sof is {}".format(url))
        response = requests.get(url=url, headers=headers, verify=settings.CERT)
        json_data = response.json()
        status = json_data.get('status', {})

        if response.status_code == 200 and status.get('code', '') == "success":
            return json_data.get('data', {})
        else:
            raise Exception(response.content)
