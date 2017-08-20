from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
import hashlib
import requests
from transaction.models import Transaction
from commision.models import Shop


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

@api_view(["POST"])
def transfer_money(request):
    shop_mobile = request.data.get("shop_mobile")
    customer_mobile = request.data.get("customer_mobile")
    amount = request.data.get("amount")
    wallet_password = request.data.get("wallet_password")
    shop = Shop.objects.get(shop_mobile=shop_mobile)
    discount = shop.discount
    paid_amount = float(amount) - (float(amount) * float(discount) / 100.00)


    #LOGIN WALLET

    api_path = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/sign-in'
    password = wallet_password
    username = customer_mobile
    password = hashlib.sha1((username + password).encode('utf-8')).hexdigest()
    params = {
        "username": username,
        "password": password,
        "type": "mobile",
        "deviceToken": "galaxyS7"
    }
    result0 = requests.post(url=api_path, headers={'Content-Type': 'application/json'}, json=params)
    result0 = result0.json()

    #TRANSFER MONEY

    # 1.Call draft transaction transfer API
    api_path_1 = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transfer/draft-transaction'
    token_wallet = result0.get('data').get('access_token')
    headers = {
        "access-token": token_wallet,
        'Content-Type': 'application/json'
    }
    params = {
        "mobileNumber": shop_mobile,
        "amount": amount,
    }
    result1 = requests.post(url=api_path_1, headers=headers, json=params)
    result1 = result1.json()
    draft_transaction_id = result1['data']['draft_transaction_id']  # "584f0e90-a886-4d34-b850-40bc1af22bbd"

    # 2.Call send OTP transfer API
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
    mobile_number = result2.get('data').get('mobile_number', '')  # '0986084686'
    otp_ref_code = result2.get('data').get('otp_ref_code', '')  # 'XNVZ'

    # 3.Call confirm OTP transfer API
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
    success = result3.get('data').get('transfer_status')  # 'Confirmed'

    tran = Transaction.objects.all().filter(customer_id=request.user, status='CONFIRMED',
                                            shop_id=shop_mobile)
    tran.status = 'PAID'
    tran.paid_amount = paid_amount
    tran.save()

    return Response({"transfer_status": success})


