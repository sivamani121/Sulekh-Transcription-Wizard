# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,CreateUserForm
from .models import  User


def login_view(request):

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
           
            user = authenticate(request,username=username, password=password)
            print(user)
            print(username, password)
            if user is not None:
                login(request, user)
                
                request.session['user_id'] = user.id
                return redirect("/")
                
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg=""
    form =None
    success=False
    form = CreateUserForm()
    if request.method == 'POST':
        userna = request.POST.get('username')
        if len(User.objects.all().filter(username=userna)) > 0:
            
            return render(request, "accounts/register.html", {"form": form,'msg':'username used '})
        
        password = request.POST.get('password1')
        email = request.POST.get('email')
        password2=request.POST.get('password2')
        if password!=password2:
             return render(request, "accounts/register.html", {"form": form,'msg':"password doesn't match"})

        response = CreateUserForm(request.POST)
        if response.is_valid():
            user = User.objects.create_user(username=userna,password=password,email=email)
            user.save()
            
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
        else:
            form = CreateUserForm()



    return render(request, "accounts/register.html", {"form": form,'msg':msg,'success':success})

def Logout(request):
    logout(request)
    return redirect('login')
