"""web_merchant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from web.views.index import health
#
# from django.contrib.auth.models import User
# from rest_framework import routers, serializers, viewsets
#
from .views import login, transfer_money
#
# # Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')
#
# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^web_affiliate/admin/', admin.site.urls),
    url(r'^web_affiliate/', include('web.urls')),
    url(r'^web_affiliate/authentications/', include('authentications.urls')),
    url(r'^web_affiliate/profile/', include('profile.urls')),
    url(r'^web_affiliate/health$', health, name="health"),
    url(r'^web_affiliate/wallet/', include('wallet.urls')),
    url(r'^web_affiliate/commision/', include('commision.urls')),
    url(r'^web_affiliate/transaction/', include('transaction.urls')),
    url(r'^web_affiliate/history', include('history.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^', include(router.urls)),
    url(r'^login', login),
    url(r'^transfer_money', transfer_money)
]
