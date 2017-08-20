from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Broker
from authentications.models import Profile
from commision.models import Customer

class InviteCustomer(TemplateView):
	template_name = 'invite_customer.html'

	def get_context(self, request, **kwargs):
		return render(request, self.template_name)
	
	def post(self, request, *args, **kwargs):
		profile = Profile.objects.get(user=self.request.user)
		username = profile.user.username

		shop_mobile = request.POST.get('shop_mobile')
		customer_mobile = request.POST.get('customer_mobile')

		customer_obj, success= Customer.objects.get_or_create(user=self.request.user)
		customer_obj.shop_mobile = shop_mobile
		customer_obj.broker_mobile = username
		customer_obj.customer_mobile = customer_mobile
		customer_obj.status = "PENDING"
		customer_obj.save()


		messages.add_message(
            request,
            messages.SUCCESS,
            'Sent the Request successfully'
        )
		return redirect('web:web-index')


