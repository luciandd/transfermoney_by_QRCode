from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from wallet.models import Wallet
import hashlib


class WalletLogin(TemplateView):
    template_name = 'login_wallet.html'

    def get_context(self, request, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        api_path = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/sign-in'
        password = request.POST.get('password')
        username = request.POST.get('username')
        password = hashlib.sha1((username+password).encode('utf-8')).hexdigest()
        params = {
            "username": username,
            "password": password,
            "type": "mobile",
            "deviceToken": "iphone7"
        }
        result = requests.post(url=api_path, headers={'Content-Type': 'application/json'}, json=params)
        result = result.json()

        token = result.get('data').get('access_token')

        # save token to db
        try:
            wallet = Wallet.objects.get(user=self.request.user)
            wallet.wallet_id = username
            wallet.token_wallet = token
            wallet.save()
        except ObjectDoesNotExist:
            Wallet.objects.create(user=self.request.user,
                                  wallet_id=username,
                                  token_wallet=token)

        messages.add_message(
            request,
            messages.SUCCESS,
            'Login Wallet successfully'
        )

        return redirect('web:web-index')
