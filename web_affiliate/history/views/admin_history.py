from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from transaction.models import Transaction
from commision.models import Shop
from authentications.models import Profile


class AdminHistory(TemplateView):
    template_name = 'admin_history.html'

    def get(self, request, *args, **kwargs):
        transactions = []
        context = super(AdminHistory, self).get_context_data(**kwargs)
        
        transaction_history = Transaction.objects.all()
        #transaction_history = Transaction.objects.all().filter(shop_id='0983655001')
        #shop = Shop.objects.get(shop_mobile='0983655001')

        for obj in transaction_history:
            print("shop id is {}".format(obj.shop_id))
            shop = Shop.objects.get(shop_mobile=obj.shop_id)
            transaction = {
                'id':obj.id,
                'bonus':shop.bonus,
                'discount':shop.discount,
                'bill_amount':obj.amount,
                'shop_id':obj.shop_id,
                'broker_id':obj.broker_id,
                'customer_id':obj.customer_id,
                'status':obj.status,
                'transaction_time':obj.transaction_time
            }
            transactions.append(transaction)

        context['transactions'] = transactions
        return render(request, 'admin_history.html', context)