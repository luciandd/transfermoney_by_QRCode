from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from wallet.utils import get_token_wallet
import requests
from django.contrib import messages
from commision.models import Shop


class Deposit(TemplateView):
    template_name = 'deposit.html'

    def get_context(self, request, **kwargs):
        token_wallet = get_token_wallet(self.request.user)
        if token_wallet:
            return render(request, self.template_name)
        else:
            return redirect('wallet:link')

    def post(self, request, *args, **kwargs):
        # api_path_4 = 'https://alp-api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/status'
        # api_path_5 = 'https://alp-api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/detail'

        #1.Call draft transaction transfer API
        api_path_1 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/draft-transaction'
        token_wallet = get_token_wallet(self.request.user)
        headers = {"access-token": token_wallet,
                   'Content-Type': 'application/json'}

        params = {
            "mobileNumber": request.POST.get('admin_id'),
            "amount": request.POST.get('bill_amount'),
        }
        result1 = requests.post(url=api_path_1, headers= headers, json=params)
        result1 = result1.json()
        print(result1)
        draft_transaction_id = result1['data']['draft_transaction_id']

        #2.Call send OTP transfer API
        api_path_2 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/get-otp'
        headers = {
            "access-token": token_wallet,
            "draft-transaction-id": draft_transaction_id,
            "Content-Type": 'application/json'
        }
        params = {
            "personalMessage": "Pay a Bill",
        }
        result2 = requests.post(url=api_path_2, headers=headers, json=params)
        result2 = result2.json()
        print(result2)
        mobile_number = result2['data'].get('mobile_number', '')
        otp_ref_code =  result2['data'].get('otp_ref_code','')

        #3.Call confirm OTP transfer API
        api_path_3 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/confirm-otp'
        params = {
            "mobile_number": mobile_number,
            "otp_ref_code": otp_ref_code,
            "otp_string": "123456"
        }
        result3 = requests.post(url=api_path_3, headers=headers, json=params)
        result3 = result3.json()
        print(result3)
        success = result3.get('data').get('transfer_status')

        if success == 'CONFIRMED':
            messages.add_message(
                request,
                messages.SUCCESS,
                'Transfer money successfully'
            )

        shop = Shop.objects.get(shop_mobile=self.request.user.username)
        shop.deposit = float(shop.deposit) + float(request.POST.get('bill_amount'))
        shop.save()

        return render(request, self.template_name)