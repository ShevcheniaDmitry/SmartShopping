from django.contrib import admin
from .models import ShoppingList, BuyList


admin.site.register(ShoppingList)
admin.site.register(BuyList)
