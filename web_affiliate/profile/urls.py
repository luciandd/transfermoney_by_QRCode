from django.conf.urls import url
from .view.detail import UserProfile
from .view.update import UserUpdate
from django.contrib.auth.decorators import login_required

app_name = 'profile'


urlpatterns = [
    url(r'^detail/$', login_required(UserProfile.as_view(), login_url='authentications:login'), name="detail"),
    url(r'^update/$', login_required(UserUpdate.as_view(), login_url='authentications:login'), name="update"),
]
