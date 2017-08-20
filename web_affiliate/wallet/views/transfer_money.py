from django.views.generic.base import TemplateView
from django.shortcuts import render,redirect
from wallet.utils import get_token_wallet
import requests
from django.contrib import messages


class Transfer_Money(TemplateView):
    template_name = 'transfer_money.html'

    def get(self, request, **kwargs):
        context = super(Transfer_Money, self).get_context_data(**kwargs)
        token_wallet = get_token_wallet(self.request.user)
        if token_wallet:
            return render(request, self.template_name, context)
        else:
            return redirect('wallet:link')

    def post(self, request, *args, **kwargs):
        # api_path_5 = 'https://alp-api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/detail'

        #1.Call draft transaction transfer API
        api_path_1 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/draft-transaction'
        token_wallet = get_token_wallet(self.request.user)
        headers = {
            "access-token": token_wallet,
            'Content-Type': 'application/json'
        }
        params = {
            "mobileNumber": request.POST.get('shop_id'),
            "amount": request.POST.get('bill_amount'),
        }
        result1 = requests.post(url=api_path_1, headers= headers, json=params)
        result1 = result1.json()
        draft_transaction_id = result1['data']['draft_transaction_id']  #"584f0e90-a886-4d34-b850-40bc1af22bbd"

        #2.Call send OTP transfer API
        api_path_2 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/get-otp'
        headers = {
            "access-token": token_wallet,
            "draft-transaction-id": draft_transaction_id,
            'Content-Type': 'application/json',
        }
        params = {
            "personalMessage": "Pay a Bill",
        }
        result2 = requests.post(url=api_path_2, headers=headers, json=params)
        result2 = result2.json()
        mobile_number = result2.get('data').get('mobile_number', '') #'0986084686'
        otp_ref_code =  result2.get('data').get('otp_ref_code','') #'XNVZ'

        #3.Call confirm OTP transfer API
        api_path_3 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/confirm-otp'
        headers = {
            "access-token": token_wallet,
            "draft-transaction-id": draft_transaction_id,
            'Content-Type': 'application/json',
        }
        params = {
            "mobile_number": mobile_number,
            "otp_ref_code": otp_ref_code,
            "otp_string": "123456"
        }
        result3 = requests.post(url=api_path_3, headers=headers, json=params)
        result3 = result3.json()
        success = result3.get('data').get('transfer_status') #'Confirmed'
        if success == 'CONFIRMED':
            messages.add_message(
                request,
                messages.SUCCESS,
                'transfer_status: CONFIRMED'
            )

        # # 4.Get status of transfer API (Optional)
        # api_path_4 = 'https://internal.tmn-dev.com/hackathon/v1/wallet/transfer/status'
        # headers = {
        #     "access-token": token_wallet,
        #     "draft-transaction-id": draft_transaction_id,
        #     'Content-Type': 'application/json',
        # }
        # result4 = requests.get(url=api_path_4, headers=headers)
        # result4 = result4.json()
        # success = result4.get('data').get('transfer_status')  # 'Confirmed'
        # if success is 'SUCCESS':
        #     messages.add_message(
        #         request,
        #         messages.SUCCESS,
        #         'transfer_status: SUCCESS'
        #     )

        return render(request, self.template_name)