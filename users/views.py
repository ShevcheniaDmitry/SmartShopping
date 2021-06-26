from django.shortcuts import render, redirect
from .forms import CreateNewUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime


def index(request):
    return render(request, 'users/main_page.html')


def inside_user(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list')
        return func(request, *args, **kwargs)
    return inner


@inside_user
def registration_user(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        form.username = request.POST['username']
        form.email = request.POST['email']
        form.password1 = request.POST['password1']
        form.password2 = request.POST['password2']
        if form.is_valid():
            form.save()
            messages.success(request, 'пользователь '+form.username+' зарегистрирован')
            return redirect('login')
    else:
        form = CreateNewUser()
    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@inside_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            messages.info(request, 'Неверно имя пользователя или пароль')
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def remember_pass(request):
    return render(request, 'users/remember_pass.html')


def new_pass(request):
    return render(request, 'users/new_pass.html')

