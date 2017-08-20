from django.views.generic.base import TemplateView
from django.shortcuts import render
import requests
from wallet.models import Wallet



class HistoryView(TemplateView):
    template_name = 'history.html'
    def get(self, request, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)

        url = 'https://api-internal.tmn-dev.com/hackathon/v1/wallet/transactions/history?startDate=2017-08-01&endDate=2017-08-30'

        wallet = Wallet.objects.get(user=self.request.user)
        token = wallet.token_wallet

        response = requests.get(url=url, headers={'access-token': token})
        data = response.json()
        context['history'] = data['data']['activities']
        return render(request, self.template_name, context)
