from django.urls import path
from . import views

urlpatterns = [
    # /auth/register
    path('register', views.register, name="register"),
    # /auth/activet_account/xyz/xyz...
    path('active_account/<uidb4>/<token>', views.active_account, name="active_account"),
    #/auth/login
    path('login/', views.login, name="login"),
    # /auth/logout
    path('logout_user/', views.logout_user, name="logout_user"),
]
