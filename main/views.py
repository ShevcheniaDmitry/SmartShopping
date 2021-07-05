from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ShoppingList, BuyList
import datetime
import codecs
from users.models import UpdateProfileForm


# функция обновления данных пользователя
def upgrade_profile(request, post):  # post = request.POST
    # если форма содержит имя пользователя, то заменяем старое имя (если оно было), на новое
    if post['nameuser']:
        request.user.profile.name = str(post['nameuser']).capitalize()  # имя с заглавной буквы
    # если пользователь вводит 'none' удаляем его имя и перестаем отображать в профиле
    if str(post['nameuser']).lower() == 'none':
        request.user.profile.name = None
    # если форма содержит фамилию пользователя, то заменяем старую фамилию (если она была), на новую
    if post['surname']:
        request.user.profile.surname = str(post['surname']).capitalize()  # фамилия с заглавной буквы
    # если пользователь вводит 'none' удаляем его фамилию и перестаем отображать в профиле
    if str(post['surname']).lower() == 'none':
        request.user.profile.surname = None
    # если форма содержит дату рождения пользователя, то заменяем старую (если она была), на новую
    if post['data']:
        request.user.profile.data = post['data']
    # если пользователь вводит сегодняшнюю дату, То удаляем его дату рождения и перестаем отображать в профиле
    if str(post['data']) == str(datetime.date.today()):
        request.user.profile.data = None
    request.user.profile.save() # сохраняем изменения имени, фамилии, даты рождения, если они были
    # если пользователь зугрузил фото, обновляем фото в profile пользователя на новое
    form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()  # сохраняем изменения в profile, если они были


@login_required(login_url='login')  # страница не доступна не авторизованному пользователю
def slist(request):
    # today - хранит всегда сегодняшнюю дату, для использования в shoppinglist.html
    # day - изначально хранит сегодняшнюю дату, но дата может быть именена пользователем, в shoppinglist.html
    today = datetime.date.today()
    day = datetime.date.today()
    if request.method == "POST":
        # если нажата кнопка 'Добавить' берем из формы данные и записываем в базу данных
        # (все поля формы обязательны для заполнения)
        if request.POST['button'] == 'Добавить':
            obj = ShoppingList(user=request.user)  # привязываем товар к пользователя, который его добавил
            obj.name = request.POST['name']
            obj.count = request.POST['count']
            obj.measure = request.POST['measure']
            obj.price = request.POST['price']
            obj.date = request.POST['data']
            if obj:
                obj.save() # сохраняем валидную форму
        # если нажата кнопка 'Готово' обновляем значение переменной day
        elif request.POST['button'] == 'Готово':
            day = request.POST['data']  # дату введенную пользователем сохраняем в переменную day
        # если не выполнились предыдущие условия, то нажата кнопка 'Удалить'
        # request.POST['button'] - содержит id товара, который необходимо удалить
        # преобразуем его в число, находим товар и удаляем его из базы данных
        else:
            ShoppingList.objects.filter(id=int(request.POST['button'])).delete()
    # при входе на страницу или после нажатия любой кнопки, заново создается список покупок пользователя date
    date = []
    for i in request.user.shoppinglist_set.all():  # проверяем все товары пользователя
        if str(day) == str(i.date):
            # едобавляем в список твоар, соответствующий дате введенной пользователем
            # (по умолчанию дата равна сегодняшнему числу)
            date.append(i)
    return render(request, 'main/shoppinglist.html', context={'date': date, 'today': today, 'day': str(day)})


@login_required(login_url='login')  # страница не доступна не авторизованному пользователю
def buy(request):
    if request.method == "POST":
        # если нажата кнопка 'Добавить' берем из формы данные и записываем в базу данных
        # (все поля формы обязательны для заполнения)
        if request.POST['button'] == 'Добавить':
            obj = BuyList(user=request.user)
            obj.name = request.POST['name']
            obj.count = request.POST['count']
            obj.measure = request.POST['measure']
            if obj:
                obj.save()
        # если нажата кнопка 'Очистить' получаем список всех товаров пользователя из базы данных buylist и удаляем их
        elif request.POST['button'] == 'Очистить':
            request.user.buylist_set.all().delete()
        # если нажата кнопка 'Очистить' получаем список всех товаров пользователя из базы данных buylist
        elif request.POST['button'] == 'Сохранить':
            # сохраняем данные в файл: static/files/list_for_user.txt
            with codecs.open(f'static/files/list_for_{str(request.user)}.txt', 'w', encoding='utf-8') as file:
                for_write = 'Список покупок: \n'
                count = 1
                products = request.user.buylist_set.all()
                for product in products:
                    for_write += str(count) + ' ' + str(product.name) + ' ' + str(product.count) + ' ' \
                                + str(product.measure) + '\n'
                    count += 1
                file.write(for_write)
        # если не выполнились предыдущие условия, то нажата кнопка 'Удалить'
        # request.POST['button'] - содержит id товара, который необходимо удалить
        # преобразуем его в число, находим товар и удаляем его из базы данных
        else:
            BuyList.objects.filter(id=int(request.POST['button'])).delete()
    # при входе на страницу или после нажатия любой кнопки, передаем на страницу список покупок из базы даннх buylist
    return render(request, 'main/buylist.html', context={'date': request.user.buylist_set.all()})


@login_required(login_url='login')  # страница не доступна не авторизованному пользователю
def profile(request):
    # если нажата кнопка 'Обновить', запускаем функцию upgrade_profile() для обновления данных профиля
    if request.method == "POST" and request.POST['button'] == 'Обновить':
        upgrade_profile(request, request.POST)
        # 'form' - форма содержащая фото пользователя
    return render(request, 'main/profile.html', context={'form': UpdateProfileForm(instance=request.user.profile)})

