from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from web.views.movement_balance.confirm import ConfirmPayment
from web.views.movement_balance.execute import ExecuteBalanceMovementView
from web.views.movement_balance.balance_movement import BalanceMovementView
from web.views.history import HistoryListView
from web.views.index import index

app_name = 'web'

urlpatterns = [
    url(r'^$', index, name="web-index"),
    url(r'^history/$', HistoryListView.as_view(), name="history"),
    url(r'^movement-balance-execution', ExecuteBalanceMovementView.as_view(), name="execute_movement_balance"),
    url(r'^order/(?P<order_id>[^/]+)/confirm$', ConfirmPayment.as_view(),
        name="confirm_order"),
    url(r'^order/(?P<order_id>[^/]+)/detail', BalanceMovementView.as_view(),
        name="cancel_movement_balance"),
]
