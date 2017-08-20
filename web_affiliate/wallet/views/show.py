from django.views.generic.base import TemplateView
from django.shortcuts import render
import requests
from django.contrib.auth.mixins import LoginRequiredMixin


class WalletView(TemplateView):
    template_name = 'login_wallet.html'
    def get_context(self, request, **kwargs):
        #get data from db


        return render(request, self.template_name,)
