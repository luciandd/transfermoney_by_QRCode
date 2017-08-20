from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from commision.models import Fee
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


class CommissionFee(TemplateView):
    template_name = 'commission_fee.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        fee = request.POST.get('fee')

        try:
            commission = Fee.objects.get(pk=1)
            commission.fee = fee
            commission.save()
        except ObjectDoesNotExist:
            Fee.objects.create(fee=fee)

        messages.add_message(
            request,
            messages.SUCCESS,
            'Save Commission Fee successfully'
        )

        return redirect('web:web-index')
