from django.shortcuts import render, redirect
from .forms import CreateNewUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile


def index(request):
    return render(request, 'users/main_page.html')


def inside_user(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list')
        return func(request, *args, **kwargs)
    return inner


def form_errors(request, errors):
    if 'Пользователь с таким именем уже существует' in errors:
        messages.error(request, 'Пользователь c таким именем уже зарегистрирован')
    elif 'username' in errors:
        messages.error(request, 'Недопустимое имя пользователя')
    elif 'email' in errors:
        messages.error(request, 'Неверный адресс электронной почты')
    elif 'Введенные пароли не совпадают' in errors:
        messages.error(request, 'Введенные пароли не совпадают')
    elif 'password' in errors:
        messages.error(request, 'Пароль слишком простой')
    else:
        messages.error(request, 'Ошибка заполнения формы')


@inside_user
def registration_user(request):
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        form.username = request.POST['username']
        form.email = request.POST['email']
        form.password1 = request.POST['password1']
        form.password2 = request.POST['password2']
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'пользователь ' + str(user) + ' зарегистрирован')
            return redirect('login')
        else:
            form_errors(request, str(form.errors))
    else:
        form = CreateNewUser()
    return render(request, 'users/registration.html', context={'form': form})


@inside_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('buy')
        else:
            messages.info(request, 'Неверно имя пользователя или пароль')
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')




