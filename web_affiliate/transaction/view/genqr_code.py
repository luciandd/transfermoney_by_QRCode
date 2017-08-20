from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from transaction.models import Transaction
from commision.models import Shop
import pyqrcode as decrype_qr


class GenGR_Code(TemplateView):
    template_name = 'gengr_code.html'

    def get(self, request, **kwargs):
        context = super(GenGR_Code, self).get_context_data(**kwargs)
        transaction_id = context['transaction_id']
        objs= Transaction.objects.get(id=int(transaction_id))
        shop_id = objs.shop_id
        shop = Shop.objects.get(shop_mobile=shop_id)
        amount = int(objs.amount)
        discount = int(shop.discount)
        pay = caculate_pay(amount, discount)
        context.update({
            'bill_amount': amount,
            'discount': discount,
            'pay': pay,
        })

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = super(GenGR_Code, self).get_context_data(**kwargs)

        transaction_id = context['transaction_id']
        objs= Transaction.objects.get(id=int(transaction_id))
        shop_id = objs.shop_id
        shop = Shop.objects.get(shop_mobile=shop_id)
        amount = int(objs.amount)
        discount = int(shop.discount)
        pay = caculate_pay(amount, discount)

        code = {
            'amount': request.POST.get('pay'),
            'mobileNumber': shop.shop_mobile
        }
        code = decrype_qr.create(str(code))
        code.png('./static/media/deadpool.png', scale=5)

        
        context.update({
            'bill_amount': amount,
            'discount': discount,
            'pay': pay,
        })
        context['loaded_image'] = 1
        return render(request, self.template_name, context)


def caculate_pay(amount, discount):
    pay = amount - (amount * discount / 100.00)
    return pay
