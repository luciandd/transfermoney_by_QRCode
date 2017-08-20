from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from transaction.models import Transaction
from datetime import datetime
from django.contrib import messages


class Discount(TemplateView):
    template_name = 'discount.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        shop_id = request.POST.get('shop_id')
        bill_amount = request.POST.get('bill_amount')

        new_value = Transaction(shop_id=shop_id, customer_id=self.request.user ,amount=bill_amount, status='PENDING', transaction_time=datetime.now())
        new_value.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Sent the Request successfully'
        )

        return redirect('web:web-index')
