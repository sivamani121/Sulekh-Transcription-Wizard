# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,CreateUserForm
from .models import Users


def login_view(request):

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username, password=password)
            print(username, password)
            if user is not None:
                login(request, user)
                y = Users.objects.all().filter(username=username,password=password).first()
                request.session['user_id'] = user.id
                request.session['users_id'] = y.id
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        email = request.POST.get('email')
        response = CreateUserForm(request.POST)
        if response.is_valid():
            y = Users(username=username, password=password, email=email)
            y.save()
            response.save()


    return render(request, "accounts/register.html", {"form": form})

def Logout(request):
    logout(request)
    return redirect('login')
