from authentications.models import Authentications
from web_affiliate.utils import setup_logger
from web_affiliate import api_settings

from django.conf import settings
from authentications.utils import get_auth_header
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

import logging
import requests
import uuid

logger = logging.getLogger(__name__)


class ExecuteBalanceMovementView(LoginRequiredMixin, TemplateView):
    template_name = "movement_balance/execute_page.html"
    login_url = 'authentications:login'
    redirect_field_name = 'next'
    _services_list = {}
    company_agent_id = "1"
    logger = logger
    order_url = settings.HOST_NAMES + "payment/" + api_settings.API_VERSION + "/orders/normals"

    def dispatch(self, request, *args, **kwargs):
        self.logger = setup_logger(request, logger)
        return super(ExecuteBalanceMovementView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.logger.info('========== Start display movement balance execute page ==========')
        service_list = self._get_services_list()
        sof_list = self._get_sof_types_list()
        data = {'service_list': service_list, 'sof_list': sof_list}
        self.logger.info('========== End display movement balance execute page ==========')
        return data

    def post(self, request, *args, **kwargs):
        self.logger.info('========== Start execute movement balance from company agent to other agent==========')

        service_id = request.POST.get('service_id')

        # payer
        payer_id = request.POST.get('payer_id')
        payer_sof_type = request.POST.get('payer_sof_type_id')
        payer_sof_id = request.POST.get('payer_sof_id')

        # payee
        sof_type = request.POST.get('sof_type')
        payee_id = request.POST.get('payee_id')
        sof_id = request.POST.get('sof_id')
        amount = request.POST.get('amount')
        payee_user_type_id = request.POST.get('payee_user_type_id')

        self.logger.info("service is - {}".format(self._services_list.get(service_id)))
        service = self._get_service_objects(service_id)
        sof = self._get_sof_objects(sof_type)
        user = Authentications.objects.get(user=self.request.user)
        ext_transaction_id = uuid.uuid4()

        payee_user_type = ''
        if payee_user_type_id == '1':
            payee_user_type = 'customer'
        elif payee_user_type_id == '2':
            payee_user_type = 'agent'

        data = {
            "ext_transaction_id": str(ext_transaction_id),
            "product_service": {
                "id": service.get("service_id"),
                "name": service.get("service_name"),
                "currency": service.get("currency")
            },
            "product": {
                "product_name": "Product name",
                "product_ref1": "Reference 1",
                "product_ref2": "Reference 2",
                "product_ref3": "Reference 3",
                "product_ref4": "Reference 4",
                "product_ref5": "Reference 5"
            },
            "payer_user": {
                "ref": {
                    "type": "access token",
                    "value": user.access_token
                },
            },
            "payee_user": {
                "user_id": payee_id,
                "user_type": payee_user_type
            },
            "amount": float(amount)
        }
        headers = self._get_headers()
        url = self.order_url

        self.logger.info("Request: {}".format(data))

        response = requests.post(url=url, json=data, headers=headers, verify=settings.CERT)

        json_data = response.json()
        self.logger.info("Response status from backend {}".format(response.content))
        status = json_data.get('status', {})

        if response.status_code == 200 and status.get('code', '') == "success":
            self.logger.info('========== End execute movement balance from company agent to other agent==========')
            return redirect('web:history')
        else:
            raise Exception(response.content)

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

    def _get_headers(self):
        if getattr(self, '_headers', None) is None:
            self._headers = get_auth_header(self.request, self.request.user)
        return self._headers

    def _get_services_list(self):
        if getattr(self, '_services', None) is None:
            self.logger.info("Getting equator service list by {} user id".format(self.request.user.username))
            headers = self._get_headers()
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
            headers = self._get_headers()
            response = requests.get(url, headers=headers, verify=settings.CERT)
            self.logger.info("Get sof type list response data is {}".format(response.content))
            json_data = response.json()
            self.logger.info("Response status code: {}".format(response.status_code))
            self._sof_type = json_data['data']
        return self._sof_type
