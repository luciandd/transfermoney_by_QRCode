from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views.shop_history import ShopHistory
from .views.customer_history import CustomerHistory
from .views.broker_history import BrokerHistory
from .views.admin_history import AdminHistory


app_name = 'history'


urlpatterns = [
    url(r'^shop_history/$', login_required(ShopHistory.as_view(), login_url='authentications:login'), name="shop_history"),
    url(r'^customer_history/$', login_required(CustomerHistory.as_view(), login_url='authentications:login'), name="customer_history"), 
    url(r'^broker_history/$', login_required(BrokerHistory.as_view(), login_url='authentications:login'), name="broker_history"),
    url(r'^admin_history/$', login_required(AdminHistory.as_view(), login_url='authentications:login'), name="admin_history"),    
]





