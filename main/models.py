from django.db import models
from django.contrib.auth.models import User


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    measure = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.name) + '  ' + str(self.date)

    def delete(self, *args, **kwargs):
        self.name.delete()
        self.count.delete()
        self.measure.delete()
        self.price.delete()
        self.date.delete()
        super().delete(*args, **kwargs)


class BuyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    measure = models.CharField(max_length=50)

    def delete(self, *args, **kwargs):
        self.name.delete()
        self.count.delete()
        self.measure.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)


