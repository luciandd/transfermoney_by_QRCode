from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from transaction.models import Transaction
from commision.models import Shop
from authentications.models import Profile


class BrokerHistory(TemplateView):
    template_name = 'broker_history.html'

    def get(self, request, *args, **kwargs):
        transactions = []
        context = super(BrokerHistory, self).get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        username = profile.user.username
        
        transaction_history = Transaction.objects.all().filter(broker_id=username)
        
        #transaction_history = Transaction.objects.all().filter(shop_id='0983655001')
        #shop = Shop.objects.get(shop_mobile='0983655001')

        for obj in transaction_history:
            shop = Shop.objects.get(shop_mobile=obj.shop_id)
            transaction = {
                'id':obj.id,
                'bonus':shop.bonus,
                'discount':shop.discount,
                'bill_amount':obj.amount,
                'shop_id':obj.shop_id,
                'customer_id':obj.customer_id,
                'status':obj.status,
                'transaction_time':obj.transaction_time
            }
            transactions.append(transaction)

        context['transactions'] = transactions
        return render(request, 'broker_history.html', context)