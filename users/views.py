from django.shortcuts import render, redirect
from .forms import CreateNewUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile


# Функция загрузки стартовой страницы проекта 'home'
def index(request):
    return render(request, 'users/main_page.html')


# Декоратор - если пользователь Авторизовался, ему не доступны страницы Регистрации и Авторизации
# Перебросит пользователя на список покупок 'list'
def inside_user(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list')
        return func(request, *args, **kwargs)
    return inner


# Функция обработки ошибок при регистрации пользователя
def form_errors(request, errors):  # errors - ошибки формы преобразованные в строку
    #  если errors содержит определенный текст ошибки, то отправляется messages в registration.html
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
    # Сообщение для других, не описанных выше ошибок (если они есть)
    else:
        messages.error(request, 'Ошибка заполнения формы')


@inside_user
def registration_user(request):
    if request.method == 'POST':
        # заполняем форму данными, полученными из request.POST
        form = CreateNewUser(request.POST)
        form.username = request.POST['username']
        form.email = request.POST['email']
        form.password1 = request.POST['password1']
        form.password2 = request.POST['password2']
        if form.is_valid():
            user = form.save()  # если форма верная, то сохраняем ее
            Profile.objects.create(user=user)  # создаем Profile для нового пользователя
            # отправляем сообщение в login.html и переходим на эту страницу
            messages.success(request, 'пользователь ' + str(user) + ' зарегистрирован')
            return redirect('login')
        # если форма не валидная, запускаем функцию form_errors(), в которую передаем ошибку в виде строки
        else:
            form_errors(request, str(form.errors))
    else:
        form = CreateNewUser()
    return render(request, 'users/registration.html', context={'form': form})


@inside_user
def login_user(request):
    if request.method == 'POST':
        # пользователь вводит свои данные логин и пароль
        username = request.POST['username']
        password = request.POST['password']
        # проверяем, есть ли пользователь с такими данными в базе
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # если пользователь с введенными данными существует, выполняем login, и переходим на страницу 'buy'
            login(request, user)
            return redirect('buy')
        else:
            # если пользователь не найден в базе, отправим messages на страницу login.html
            messages.info(request, 'Неверно имя пользователя или пароль')
    return render(request, 'users/login.html')


# При нажатии кнопки Выход, выполняем logout пользователя и переходим на страницу 'login'
def logout_user(request):
    logout(request)
    return redirect('login')




