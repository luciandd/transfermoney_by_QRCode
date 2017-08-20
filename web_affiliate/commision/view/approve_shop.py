from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Shop
from authentications.models import Profile


class Approve_Shop(TemplateView):
    template_name = 'approve_shop.html'

    def get(self, request, *args, **kwargs):
        context = super(Approve_Shop, self).get_context_data(**kwargs)

        shops_list = []
        shops_obj = Shop.objects.all().filter(status='pending')

        for obj in shops_obj:
            shop = {'shop_id':obj.shop_id,
                    'bonus':int(obj.bonus),
                    'discount':int(obj.discount),
                    'status':obj.status,
                    'shop_name': obj.shop_name,
                    'shop_mobile': obj.shop_mobile,
                    'deposit': int(obj.deposit),
                    }
            shops_list.append(shop)

        context['shops'] =  shops_list

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        confirmed_checkbox = request.POST.getlist('checkbox')
        checkbox_list = [int(i) for i in confirmed_checkbox]

        shops_obj = Shop.objects.all().filter(status='pending')
        for obj in shops_obj:
            if obj.shop_id in checkbox_list:
                obj.status = 'confirmed'
                shop = Profile.objects.get(user_id=obj.user_id)
                is_shop = "is_shop"
                if not shop.permissions:
                    shop.permissions = [is_shop]
                elif is_shop not in shop.permissions:
                    shop.permissions.append(is_shop)
                shop.save()
                obj.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Approve Shop successfully'
        )
        return redirect('commision:approve_shop')

