from django.db import models
from django.contrib.auth.models import User


# База данных для сохранения списка товаров, товаров у каждого пользователя может быть много
class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    measure = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False)

# В админ панели отображается как: название товара и дата
    def __str__(self):
        return str(self.name) + '  ' + str(self.date)

# При удалении пользователя удаляется список его товаров
    def delete(self, *args, **kwargs):
        self.name.delete()
        self.count.delete()
        self.measure.delete()
        self.price.delete()
        self.date.delete()
        super().delete(*args, **kwargs)


# База данных для сохранения покупок, покупок у каждого пользователя может быть много
class BuyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    measure = models.CharField(max_length=50)

# В админ панели отображается как: название товара
    def __str__(self):
        return str(self.name)

# При удалении пользователя удаляется список его покупок
    def delete(self, *args, **kwargs):
        self.name.delete()
        self.count.delete()
        self.measure.delete()
        super().delete(*args, **kwargs)

