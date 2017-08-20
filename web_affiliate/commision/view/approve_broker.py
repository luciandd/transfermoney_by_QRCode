from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Broker
from authentications.models import Profile

class Approve_Broker(TemplateView):
	template_name = 'approve_broker.html'

	def get(self, request, *args, **kwargs):
		context = super(Approve_Broker, self).get_context_data(**kwargs)
		broker_list = []

		profile = Profile.objects.get(user=self.request.user)
		username = profile.user.username 

		broker_obj = Broker.objects.all().filter(status='pending', shop_mobile=username)
		for obj in broker_obj:
			broker = {
			'broker_id': obj.id,
			'shop_mobile': obj.shop_mobile,
			'broker_mobile': obj.broker_mobile,
			'broker_name': obj.broker_name,
			'broker_email': obj.broker_email,
			'status': obj.status,
			}
			broker_list.append(broker)

		context['brokers'] = broker_list
		return render(request, 'approve_broker.html', context)

	def post(self, request, *args, **kwargs):
		profile = Profile.objects.get(user=self.request.user)
		username = profile.user.username
		
		confirmed_checkbox = request.POST.getlist('checkbox')

		checkbox_list = [int(i) for i in confirmed_checkbox]

		broker_obj = Broker.objects.all().filter(status='pending', shop_mobile=username)

		for obj in broker_obj:
			if obj.id in checkbox_list:
				obj.status = 'CONFIRMED'
				broker = Profile.objects.get(user_id=obj.user_id)
				is_broker = "is_broker"
				if not broker.permissions:
					broker.permissions = [is_broker]
				elif is_broker not in broker.permissions:
					broker.permissions.append(is_broker)
				broker.save()
				obj.save()

		# broker = Profile.objects.get(user=self.request.user)
		messages.add_message(
			request,
			messages.SUCCESS,
			'Approve Broker Successfully'
		)
		return redirect("commision:approve_broker")
