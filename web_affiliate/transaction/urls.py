from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .view.confirmation import Confirmation
from .view.payment import Payment
from .view.discount import Discount
from .view.genqr_code import GenGR_Code

app_name = 'transaction'


urlpatterns = [
    url(r'^confirmation/$', login_required(Confirmation.as_view(), login_url='authentications:login'), name="confirm_transaction"),
    url(r'^confirmation/genqr_code/(?P<transaction_id>[0-9A-Za-z]+)/$', login_required(GenGR_Code.as_view(), login_url='authentications:login'), name="genqr_code"),
    url(r'^payment/$', login_required(Payment.as_view(), login_url='authentications:login'), name="payment"),
    url(r'^discount/$', login_required(Discount.as_view(), login_url='authentications:login'), name="discount"),
]
