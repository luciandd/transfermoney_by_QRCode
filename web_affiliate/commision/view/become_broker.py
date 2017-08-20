from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Broker
from authentications.models import Profile


class Become_Broker(TemplateView):
    template_name = 'become_broker.html'

    def get_context(self, request, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):

        broker, success = Broker.objects.get_or_create(user=self.request.user)
        broker_info, success = Profile.objects.get_or_create(user=self.request.user)
        broker.broker_name = broker_info.user.first_name
        broker.broker_mobile = broker_info.user.username
        broker.broker_email = broker_info.user.email
        broker.shop_mobile = request.POST.get('shop_mobile')
        broker.status = "PENDING"
        broker.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Sent the Request successfully'
        )
        return redirect('web:web-index')

