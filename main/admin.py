from django.contrib import admin
from .models import ShoppingList, BuyList


admin.site.register(ShoppingList)  # Добавление ShoppingList в панель администратора
admin.site.register(BuyList)  # Добавление BuyList в панель администратора

