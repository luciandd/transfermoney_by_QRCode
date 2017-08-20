from django.contrib.auth import logout
from .models import Authentications
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserRegisterForm
from hashlib import sha256
from django.contrib import messages


def login_form(request):
    user = None
    if request.user.is_authenticated():
        return redirect('web:web-index')
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('web:web-index')
    return render(request, "authentications/login.html", {})


def logout_form(request):
    logout(request)
    print("Logout success")
    return render(request, "authentications/login.html", {})


def register_form(request):
    user = None
    if request.user.is_authenticated():
        return redirect('web:web-index')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                username = form.cleaned_data.get("username")
                first_name = form.cleaned_data['first_name']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    'Registration successfully'
                )
            return render(request, "authentications/login.html", {})
        else:
            form = UserRegisterForm()
            return render(request, "authentications/register.html", {})
