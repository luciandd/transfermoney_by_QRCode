from wallet.views.create import WalletCreate
from wallet.views.login import WalletLogin
from wallet.views.topup import Topup
from wallet.views.transfer_money import Transfer_Money
from wallet.views.deposit import Deposit
from wallet.views.history import HistoryView
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


app_name = 'wallet'
login_url = 'authentications:login'

urlpatterns = [
    url(r'^create', login_required(WalletCreate.as_view(), login_url='authentications:login'), name="create"),
    url(r'^login', login_required(WalletLogin.as_view(), login_url='authentications:login'), name="login"),
    url(r'^topup', login_required(Topup.as_view(), login_url='authentications:login'), name="topup"),
    url(r'^transfer_money', login_required(Transfer_Money.as_view(), login_url='authentications:login'), name="transfer_money"),
    url(r'^deposit', login_required(Deposit.as_view(), login_url='authentications:login'), name="deposit"),
    url(r'^history', login_required(HistoryView.as_view(), login_url='authentications:login'), name="history"),
]