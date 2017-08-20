from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Customer
from authentications.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class Approve_Invite_Broker(TemplateView):
    template_name = 'approve_invite_broker.html'

    def get(self, request, *args, **kwargs):
        context = super(Approve_Invite_Broker, self).get_context_data(**kwargs)

        invite_list = []
        profile = Profile.objects.get(user=self.request.user)
        customer_name = profile.user.username

        invite_obj = Customer.objects.all().filter(status='pending', customer_mobile=customer_name)
        for obj in invite_obj:
        	shop = User.objects.get(username=obj.shop_mobile)
        	shop_name = shop.first_name
        	broker = User.objects.get(username=obj.broker_mobile)
        	broker_name = broker.first_name

        	customers = {
        		'id': obj.id,
        		'broker_name': broker_name,
        		'broker_mobile': obj.broker_mobile,
        		'shop_name': shop_name,
        		'shop_mobile': obj.shop_mobile,
        		'shop_address': '',
        		'status': obj.status,
        	}
        	invite_list.append(customers)
        context['customers'] = invite_list
        return render(request, 'approve_invite_broker.html', context)

    def post(self, request, *args, **kwargs):
        confirmed_checkbox = request.POST.getlist('checkbox')
        checkbox_list = [int(i) for i in confirmed_checkbox]
        invite_obj = Customer.objects.all().filter(status='pending')
        for obj in invite_obj:
            if obj.id in checkbox_list:
                obj.status = 'confirmed'
                customer = Profile.objects.get(user=self.request.user)
                is_customer = "is_customer"
                if not customer.permissions:
                    customer.permissions['is_customer']
                elif customer not in customer.permissions:
                    customer.permissions.append(is_customer)
                customer.save()
                obj.save()

        messages.add_message(
			request,
			messages.SUCCESS,
			'Approve Broker Successfully'
		)
        return redirect("commision:approve_invite_broker")

