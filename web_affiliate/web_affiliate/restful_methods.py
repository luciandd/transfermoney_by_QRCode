import time
import requests
import json
from decimal import Decimal

from django.conf import settings
from web_admin.utils import setup_logger
from web_admin.get_header_mixins import GetHeaderMixin
from authentications.apps import InvalidAccessToken


class RESTfulMethods(GetHeaderMixin):
    def _get_method(self, api_path, func_description=None, logger=None, is_getting_list=False, params={}, timeout=None):
        """
        :param api_path: 
        :param func_description: 
        :param logger: 
        :param is_getting_list: 
        :param params: 
        :return: 
        """

        if 'http' in api_path:
            url = api_path
        else:
            url = settings.DOMAIN_NAMES + api_path

        if timeout is None:
            timeout = settings.GLOBAL_TIMEOUT

        try:
            if len(params) > 0:
                self.logger.info("Params: {} ".format(params))
            self.logger.info('API-Path: {path}'.format(path=url))
            start_time = time.time()
            response = requests.get(url, headers=self._get_headers(), verify=settings.CERT, timeout=timeout)
            end_time = time.time()
            processing_time = end_time - start_time
            http_status_code = response.status_code

            self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))
            self.logger.info('Processing time: [{processing_time}]'.format(processing_time=processing_time))

            response_json = response.json()
            response_json['status_code'] = response.status_code

            try:
                status = response_json.get('status', {})
                code = status.get('code', '')
                message = status.get('message', '')
            except Exception as e:
                self.logger.error(e)
                raise Exception(response.content)

            self.logger.info("Status code [{}] and message [{}]".format(code, message))
            if response.status_code == 200 and code == "success":
                if is_getting_list:
                    default_type = []
                else:
                    default_type = {}
                data = response_json.get('data', default_type)

                # self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))
                if is_getting_list:
                    self.logger.info('Response_content_count: {}'.format(len(data)))
                else:
                    self.logger.info('Response_content: {}'.format(data))
                # self.logger.info('Response_time: {}'.format(end_time - start_time))

                result = data, True
            else:
                message = status.get('message', '')
                if code in ["access_token_expire", 'authentication_fail', 'invalid_access_token',
                            'authentication_fail']:
                    self.logger.info("{} for {} username".format(message, self.request.user))
                    raise InvalidAccessToken(message)
                if message:
                    result = message, False
                else:
                    raise Exception(response.content)
        except requests.exceptions.Timeout:
            result = 'timeout', False

        return result

    def _put_method(self, api_path, func_description, logger=None, params={}, timeout=None):
        """
        :param api_path: the API path
        :param func_description: the description of method, used for logging
        :param logger: the logger object to print log
        :param params: the data of put method
        :return: data and success (True or False)
        """

        if 'http' in api_path:
            url = api_path
        else:
            url = settings.DOMAIN_NAMES + api_path

        if timeout is None:
            timeout = settings.GLOBAL_TIMEOUT
        
        self.logger.info("Params: {} ".format(params))
        self.logger.info('API-Path: {path}'.format(path=api_path))
        try:
            start_date = time.time()
            response = requests.put(url, headers=self._get_headers(), json=params, verify=settings.CERT,
                                    timeout=timeout)
            done = time.time()
            processing_time = done - start_date
            http_status_code = response.status_code
            # Filter sensitive data
            self._filter_sensitive_fields(params=params)
            self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))
            
            self.logger.info('Processing time: [{processing_time}]'.format(processing_time=processing_time))

            try:
                response_json = response.json()
                status = response_json.get('status', {})
                code = status.get('code', '')
                message = status.get('message', '')
            except Exception as e:
                self.logger.error(e)
                raise Exception(response.content)
            self.logger.info("Status code [{}] and message [{}]".format(code, message))
            if code == "success":
                result = response_json.get('data', {}), True
                self.logger.info('Response_content: {}'.format(result[0]))
            else:
                message = status.get('message', '')
                if code in ["access_token_expire", 'authentication_fail', 'invalid_access_token',
                            'authentication_fail']:
                    self.logger.info("{} for {} username".format(message, self.request.user))
                    raise InvalidAccessToken(message)

                if message:
                    result = message, False
                else:
                    raise Exception(response.content)
        except requests.exceptions.Timeout:
            result = 'timeout', False

        return result

    def _post_method(self, api_path, func_description=None, logger=None, params={}, only_return_data=True,
                     timeout=None):
        """
        :param api_path: 
        :param func_description: 
        :param logger: 
        :param params: 
        :return: 
        """

        if 'http' in api_path:
            url = api_path
        else:
            url = settings.DOMAIN_NAMES + api_path

        if timeout is None:
            timeout = settings.GLOBAL_TIMEOUT
        
        self.logger.info("Params: {} ".format(params))
        self.logger.info('API-Path: {path}'.format(path=api_path))
        try:
            start_time = time.time()
            response = requests.post(url, headers=self._get_headers(), json=params, verify=settings.CERT,
                                     timeout=timeout)
            end_time = time.time()
            processing_time = end_time - start_time
            http_status_code = response.status_code
            # Filter sensitive data
            self._filter_sensitive_fields(params=params)

            self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))

            response_json = response.json()
            self.logger.info('Processing time: [{processing_time}]'.format(processing_time=processing_time))
            response_json['status_code'] = response.status_code

            try:
                status = response_json.get('status', {})
                code = status.get('code', '')
                message = status.get('message', '')
            except Exception as e:
                self.logger.error(e)
                raise Exception(response.content)
            self.logger.info("Status code [{}] and message [{}]".format(code, message))
            if code == "success":
                data = response_json.get('data', {})
                if isinstance(data, list) and len(data) > 1:
                    self.logger.info("Response_content_count: {}".format(len(data)))
                else:
                    self.logger.info("Response_content: {}".format(data))
                if only_return_data:
                    result = data, True
                else:
                    result = response_json, True
            else:
                self.logger.info("Response_content: {}".format(response.text))
                message = status.get('message', '')
                if code in ["access_token_expire", 'authentication_fail', 'invalid_access_token',
                            'authentication_fail']:
                    self.logger.info("{} for {} username".format(message, self.request.user))
                    raise InvalidAccessToken(message)

                if message:
                    result = message, False
                else:
                    raise Exception(response.content)
        except requests.exceptions.Timeout:
            result = 'timeout', False

        return result

    def _delete_method(self, api_path, func_description, logger=None, params={}, timeout=None):

        if 'http' in api_path:
            url = api_path
        else:
            url = settings.DOMAIN_NAMES + api_path

        if timeout is None:
            timeout = settings.GLOBAL_TIMEOUT

        self.logger.info('API-Path: {path}'.format(path=api_path))
        try:
            start_time = time.time()
            response = requests.delete(url, headers=self._get_headers(), json=params, verify=settings.CERT,
                                       timeout=timeout)
            end_time = time.time()
            processing_time = end_time - start_time
            http_status_code = response.status_code
            self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))
            self.logger.info('Processing time: [{processing_time}]'.format(processing_time=processing_time))

            response_json = response.json()
            try:
                status = response_json.get('status', {})
                code = status.get('code', '')
                message = status.get('message', '')
            except Exception as e:
                self.logger.error(e)
                raise Exception(response.content)

            self.logger.info("Status code [{}] and message [{}]".format(code, message))
            if code == "success":
                result = response_json.get('data', {}), True
                self.logger.info("Response_content: {}".format(result[0]))
            else:
                message = status.get('message', '')
                if code in ["access_token_expire", 'authentication_fail', 'invalid_access_token',
                            'authentication_fail']:
                    raise InvalidAccessToken(message)
                if message:
                    result = message, False
                else:
                    raise Exception(response.content)
        except requests.exceptions.Timeout:
            result = 'timeout', False

        return result

    def _get_precision_method(self, api_path, func_description, logger=None, is_getting_list=False, params={}):
        """
        :param api_path: 
        :param func_description: 
        :param logger: 
        :param is_getting_list: 
        :param params: 
        :return: 
        """

        if 'http' in api_path:
            url = api_path
        else:
            url = settings.DOMAIN_NAMES + api_path
            
        if len(params) > 0:
            self.logger.info("Params: {} ".format(params))
        self.logger.info('API-Path: {path}'.format(path=url))
        start_date = time.time()
        response = requests.get(url, headers=self._get_headers(), verify=settings.CERT)
        done = time.time()
        http_status_code = response.status_code
        processing_time = done - start_date
        self.logger.info('Result is [{http_status_code}] HTTP status code.'.format(http_status_code=http_status_code))
        self.logger.info('Processing time: [{processing_time}]'.format(processing_time=processing_time))
        try:
            response_json = json.loads(response.text, parse_float=Decimal)
            status = response_json.get('status', {})
            code = status.get('code', '')
            message = status.get('message', '')
        except Exception as e:
            self.logger.error(e)
            raise Exception(response.content)
        self.logger.info("Status code [{}] and message [{}]".format(code, message))
        if response.status_code == 200 and code == "success":
            if is_getting_list:
                default_type = []
            else:
                default_type = {}
            data = response_json.get('data', default_type)
            if is_getting_list:
                self.logger.info('Response_content_count: {}'.format(len(data)))
            else:
                self.logger.info('Response_content: {}'.format(data))
            result = data, True
        else:
            message = status.get('message', '')
            if (code == "access_token_expire") or (code == 'authentication_fail') or (
                        code == 'invalid_access_token'):
                self.logger.info("{} for {} username".format(message, self.request.user))
                raise InvalidAccessToken(message)
            if message:
                result = message, False
            else:
                raise Exception(response.content)
        return result

    @staticmethod
    def _filter_sensitive_fields(params={}):

        if 'password' in params:
            params['password'] = '******'

        if 're-password' in params:
            params['re-password'] = '******'

        return params;
