from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from transaction.models import Transaction
from django.contrib import messages


class Confirmation(TemplateView):
    template_name = 'confirmation.html'

    def get(self, request, **kwargs):
        context = super(Confirmation, self).get_context_data(**kwargs)
        trans_list = []
        trans = Transaction.objects.all().filter(shop_id=self.request.user, status='PENDING')
        for obj in trans:
            trans_list.append(
                {
                    'id': obj.id,
                    'bill_amount': int(obj.amount),
                    'status': obj.status,
                    'customer': obj.customer_id,
                }
            )
        context['confirm'] = trans_list
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        confirmed_checkbox = request.POST.getlist('checkbox')
        checkbox_list = [int(i) for i in confirmed_checkbox]

        for id in checkbox_list:
            obj = Transaction.objects.get(pk=id)
            obj.status = 'CONFIRMED'
            obj.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Confirm discount successfully'
        )
        return redirect('transaction:confirm_transaction')
