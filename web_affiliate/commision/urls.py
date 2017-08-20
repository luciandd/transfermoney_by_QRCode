from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .view.become_shop import Become_Shop
from .view.become_broker import Become_Broker
from .view.approve_shop import Approve_Shop
from .view.invite_customer import InviteCustomer
from .view.approve_broker import Approve_Broker
from .view.approve_invite_broker import Approve_Invite_Broker
from .view.commission_fee import CommissionFee


app_name = 'commision'

urlpatterns = [
    url(r'^become_shop/$', login_required(Become_Shop.as_view(), login_url='authentications:login'), name="become_shop"),
    url(r'^become_broker/$', login_required(Become_Broker.as_view(), login_url='authentications:login'), name="become_broker"),
    url(r'^approve_shop/$', login_required(Approve_Shop.as_view(), login_url='authentications:login'), name="approve_shop"),
    url(r'^invite_customer/$', login_required(InviteCustomer.as_view(), login_url='authentications:login'), name="invite_customer"),
    url(r'^approve_broker/$', login_required(Approve_Broker.as_view(), login_url='authentications:login'), name="approve_broker"),
    url(r'^approve_invite_broker/$', login_required(Approve_Invite_Broker.as_view(), login_url='authentications:login'), name="approve_invite_broker"),
    url(r'^fee/$', login_required(CommissionFee.as_view(), login_url='authentications:login'), name="commission_fee"),
]
