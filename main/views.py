from django.shortcuts import render
from .models import ShoppingList
import datetime


def list_shop(day, username):
    date = []
    for i in ShoppingList.objects.all():
        if i.user == username and str(day) == str(i.date):
            date.append(i)
    return date


def slist(request):
    today = datetime.date.today()
    day = datetime.date.today()
    username = request.user.username
    if request.method == "POST":
        print(request.POST)
        try:
            obj = ShoppingList()
            obj.name = request.POST['name']
            obj.count = request.POST['count']
            obj.measure = request.POST['measure']
            obj.date = request.POST['data']
            obj.user = request.user.username
            if obj:
                obj.save()
        except:
            try:
                day = request.POST['data']
            except:
                try:
                    for i in request.POST:
                        if request.POST[i] == "Удалить":
                            dell = ShoppingList.objects.get(id=int(i))
                            dell.delete()
                except:
                    pass
    date = list_shop(day, username)
    return render(request, 'main/shoppinglist.html', context={'date': date, 'today': today, 'day': str(day)})


def buy(request):
    return render(request, 'main/buylist.html')

