from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='authentications:login')
def index(request):
    return render(request, 'web/index.html')


def health(request):
    return render(request, 'web/health.html')
