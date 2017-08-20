from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from commision.models import Shop
from django.contrib.auth import get_user_model
from authentications.models import Profile

User = get_user_model()


class Become_Shop(TemplateView):
    template_name = 'become_shop.html'

    def get(self, request, **kwargs):
        context = super(Become_Shop, self).get_context_data(**kwargs)

        profile = Profile.objects.get(user=self.request.user)

        context['shop_name'] = profile.user.first_name
        context['shop_mobile'] = profile.user.username

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):

        shop, success = Shop.objects.get_or_create(user=self.request.user)
        shop.discount = request.POST.get('discount')
        shop.bonus = request.POST.get('bonus')
        shop.shop_name= request.POST.get('shop_name')
        shop.shop_mobile = request.POST.get('shop_mobile')
        shop.shop_id = shop.user_id
        shop.status = 'pending'
        shop.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Sent the Request successfully'
        )
        return redirect('wallet:login')

