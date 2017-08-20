from authentications.models import Authentications
from web_affiliate.utils import setup_logger

from django.apps import AppConfig
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpRequest
from web_affiliate.utils import encryptText
from web_affiliate import api_settings
import requests
import logging
import time


class AuthenticationsConfig(AppConfig):
    name = 'authentications'


class InvalidAccessToken(Exception):
    """Raised when the access token is invalid"""
    pass


class InvalidAccessTokenException(object):
    def process_exception(self, request, exception):
        if type(exception) == InvalidAccessToken:
            logout(request)
            return HttpResponseRedirect(request.path)
        return None