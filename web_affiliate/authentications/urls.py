from django.conf.urls import url
from authentications.views import login_form, logout_form, register_form

app_name = 'authentications'

urlpatterns = [
    url(r'^logout/$', logout_form, name='logout'),
    url(r'^login/$', login_form, name='login'),
    url(r'^register/$', register_form, name='register'),
]
