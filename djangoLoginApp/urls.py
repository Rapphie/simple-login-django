# accounts/urls.py
from django.urls import path
from .views import (
    CustomLoginView,
    CustomSignupView,
    CustomLogoutView,
    home as home_view,
    logout_confirm as confirm,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path("logout/", CustomLogoutView.as_view(), name="account_logout"),
    path("logout_confirm", confirm, name="logout_confirm"),
    path("", home_view, name="home"),
]
