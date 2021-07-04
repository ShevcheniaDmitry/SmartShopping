from django.db import models
from django.contrib.auth.models import User
from django import forms


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile/", default='men.jpg', null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return 'Profile ' + str(self.user)

    def delete(self, *args, **kwargs):
        self.picture.delete()
        self.name.delete()
        self.surname.delete()
        self.data.delete()
        super().delete(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']

