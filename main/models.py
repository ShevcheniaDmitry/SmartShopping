from django.db import models


class ShoppingList(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    measure = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)
    user = models.CharField(max_length=50)

# picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return str(self.name) + '  ' + str(self.date)


