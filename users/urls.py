from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='home'),
    path('registration', registration_user, name='registration'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('forgot', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/login.html'),
         name='password_reset_complete'),
]
