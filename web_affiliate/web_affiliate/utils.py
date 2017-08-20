import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from django.conf import settings


def setup_logger(request, logger):
    correlation_id = request.session.get('correlation_id', '')
    client_ip = request.META['REMOTE_ADDR']
    return logging.LoggerAdapter(logger, extra={'correlationId': correlation_id, 'IPAddress': client_ip})


def encryptText(input):
    utf8_text = input.encode('utf-8')
    #pub_key = RSA.importKey(open('rsa_public.pem').read())
    pub_key = RSA.importKey(open(settings.RSA).read())
    cipher = PKCS1_v1_5.new(pub_key)
    ciphertext = base64.encodebytes(cipher.encrypt(utf8_text))
    return ciphertext.decode('utf-8')
