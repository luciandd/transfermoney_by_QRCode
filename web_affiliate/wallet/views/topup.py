from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin


class Topup(TemplateView):
    template_name = 'topup.html'

    def get_context(self, request, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        api_path = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/top-up'
        params = {
            "mobile_number": request.POST.get('mobile_number'),
            "amount": request.POST.get('amount'),
        }
        result = requests.post(api_path, json=params)
        messages.add_message(
            request,
            messages.SUCCESS,
            'Topup success'
        )
        return render(request, self.template_name)
