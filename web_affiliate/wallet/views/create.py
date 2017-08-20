from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from wallet.models import Wallet
from django.contrib import messages


class WalletCreate(LoginRequiredMixin, TemplateView):
    template_name = 'create_wallet.html'

    def get_context(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        step1 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/register/get-otp/{}'
        step2 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/register/confirm-otp'
        step3 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/register/create-profile'

        #Step 1
        params = {
            "thai_id": request.POST.get('thai_id'),
            "first_name": request.POST.get('first_name'),
            "last_name": request.POST.get('last_name'),
            "postal_code": request.POST.get('postal_code'),
            "mobile_number": request.POST.get('mobile_number'),
            "device_os": request.POST.get("device_os"),
            "password": request.POST.get('password'),
            "email": request.POST.get('email'),
            "address": request.POST.get('address'),
            "occupation": request.POST.get('occupation')
        }
        print(params)
        result1 = requests.get(url=step1.format(params['mobile_number']))
        result1_json = result1.json()
        print(result1_json)

        #Step 2
        params2 = {
            "otp_code": '123456',
            "otp_reference": result1_json['data']['otp_reference'],
            "mobile_number": params['mobile_number']
        }
        result2 = requests.post(url=step2, headers={'Content-Type': 'application/json'}, json=params2)

        result2_json = result2.json()
        print(result2_json)

        token = result2_json['data']['token']
        result3 = requests.post(step3, headers={'token': token,
                                                'Content-Type': 'application/json'}, json=params)
        result3_json = result3.json()
        print(result3_json)

        if result3_json['status_message'] == 'success':
            # Save data to db
            try:
                wallet = Wallet.objects.get(user=self.request.user)
                wallet.wallet_id = params['mobile_number']
                wallet.token_wallet = token
                wallet.save()
            except ObjectDoesNotExist:
                Wallet.objects.create(user=self.request.user,
                                      wallet_id=params['mobile_number'],
                                      token_wallet=token)


            messages.add_message(
                request,
                messages.SUCCESS,
                'Create wallet successfully'
            )
            return redirect('web:web-index')

        messages.add_message(
            request,
            messages.ERROR,
            'Please fill all fields and double check your input data.'
        )
        return redirect('wallet:create')