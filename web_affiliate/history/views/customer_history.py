from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from transaction.models import Transaction
from commision.models import Customer, Shop
from authentications.models import Profile


class CustomerHistory(TemplateView):
    template_name = 'shop_history.html'

    def get(self, request, *args, **kwargs):
        transactions = []
        context = super(CustomerHistory, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        username = profile.user.username
        
        transaction_history = Transaction.objects.all().filter(customer_id=username)
        
        for obj in transaction_history:
            shop = Shop.objects.get(shop_mobile=obj.shop_id)
            transaction = {
                'id': obj.id,
                'discount': shop.discount,
                'bill_amount': obj.amount,
                'shop_name': obj.shop_id,
                'broker_id': obj.broker_id,
                'status': obj.status,
                'transaction_time': obj.transaction_time
            }
            transactions.append(transaction)

        context['transactions'] = transactions
        return render(request, 'customer_history.html', context)





