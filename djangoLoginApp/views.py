# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy


@login_required(login_url="account_login")
def home(request):
    return render(request, "portfolio.html")


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm


class CustomSignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("account_login")

    def form_valid(self, form):
        user = form.save()
        backend = get_backends()[0]
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        login(self.request, user, backend=user.backend)
        messages.success(self.request, "Account successfully created.")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def logout_confirm(request):
    return render(request, "registration/logout_confirm.html")
