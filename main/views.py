from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ShoppingList, BuyList
import datetime
import codecs
from users.models import UpdateProfileForm


def upgrade_profile(request, post):
    if post['nameuser']:
        request.user.profile.name = str(post['nameuser']).capitalize()
    if str(post['nameuser']).lower() == 'none':
        request.user.profile.name = None
    if post['surname']:
        request.user.profile.surname = str(post['surname']).capitalize()
    if str(post['surname']).lower() == 'none':
        request.user.profile.surname = None
    if post['data']:
        request.user.profile.data = post['data']
    if str(post['data']) == str(datetime.date.today()):
        request.user.profile.data = None
    request.user.profile.save()
    form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()


@login_required(login_url='login')
def slist(request):
    today = datetime.date.today()
    day = datetime.date.today()
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        if request.POST['button'] == 'Добавить':
            obj = ShoppingList(user=request.user)
            obj.name = request.POST['name']
            obj.count = request.POST['count']
            obj.measure = request.POST['measure']
            obj.price = request.POST['price']
            obj.date = request.POST['data']
            if obj:
                obj.save()
        elif request.POST['button'] == 'Готово':
            day = request.POST['data']
        else:
            ShoppingList.objects.filter(id=int(request.POST['button'])).delete()
    date = []
    for i in request.user.shoppinglist_set.all():
        if str(day) == str(i.date):
            date.append(i)
    return render(request, 'main/shoppinglist.html', context={'date': date, 'today': today, 'day': str(day)})


@login_required(login_url='login')
def buy(request):
    if request.method == "POST":
        if request.POST['button'] == 'Добавить':
            obj = BuyList(user=request.user)
            obj.name = request.POST['name']
            obj.count = request.POST['count']
            obj.measure = request.POST['measure']
            if obj:
                obj.save()
        elif request.POST['button'] == 'Очистить':
            request.user.buylist_set.all().delete()
        elif request.POST['button'] == 'Сохранить':
            with codecs.open(f'static/files/list_for_{str(request.user)}.txt', 'w', encoding='utf-8') as file:
                for_write = 'Список покупок: \n'
                count = 1
                products = request.user.buylist_set.all()
                for product in products:
                    for_write += str(count) + ' ' + str(product.name) + ' ' + str(product.count) + ' ' \
                                + str(product.measure) + '\n'
                    count += 1
                file.write(for_write)
        else:
            BuyList.objects.filter(id=int(request.POST['button'])).delete()
    return render(request, 'main/buylist.html', context={'date': request.user.buylist_set.all()})


@login_required(login_url='login')
def profile(request):
    if request.method == "POST" and request.POST['button'] == 'Обновить':
        upgrade_profile(request, request.POST)
    return render(request, 'main/profile.html', context={'form': UpdateProfileForm(instance=request.user.profile)})

