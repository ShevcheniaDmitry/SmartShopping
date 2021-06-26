from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('registration', registration_user, name='registration'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('remember', remember_pass, name='remember_pass'),
    path('new', new_pass, name='new_pass'),
]

