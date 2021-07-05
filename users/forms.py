from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Форма для регистрации пользователя, содержит поля: 'username', 'email', 'password1', 'password2'
class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

