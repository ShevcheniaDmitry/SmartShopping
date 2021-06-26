from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="image/profile/", null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.picture.delete()
        super().delete(*args, **kwargs)


class Daylist(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    day = models.DateField(auto_now=False, auto_now_add=False)

    def delete(self, *args, **kwargs):
        self.day.delete()
        super().delete(*args, **kwargs)

