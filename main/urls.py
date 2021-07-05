from django.urls import path
from .views import *


urlpatterns = [
    path('buy', buy, name='buy'),
    path('list', slist, name='list'),
    path('profile', profile, name='profile'),

]

