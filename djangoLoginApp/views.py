# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends, authenticate
from django.utils import timezone
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import UserLoginAttempt  # Import UserProfile model
from django.contrib.auth.models import User  # Import User model


@login_required(login_url="account_login")
def home(request):
    if request.user.is_authenticated:
        current_user = request.user
    return render(request, "portfolio.html", {"current_user": current_user})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Try to get the user from the database
            user = User.objects.filter(username=username).first()

            if not user:
                # Handle case when the user doesn't exist
                messages.error(self.request, "Username does not exist.")
                return self.form_invalid(form)

            # Handle lockout
            profile, created = UserLoginAttempt.objects.get_or_create(user=user)
            if profile.is_locked_out():
                remaining_time = profile.lockout_until - timezone.now()
                total_seconds = int(remaining_time.total_seconds())
                minutes, seconds = divmod(total_seconds, 60)
                messages.error(
                    self.request,
                    f"Account is locked. Try again in {int(minutes)} minutes and {int(seconds)} seconds.",
                )
                return self.form_invalid(form)

            # Attempt to authenticate the user
            authenticated_user = authenticate(
                self.request, username=username, password=password
            )

            if authenticated_user is not None:
                # Successful login, reset failed attempts
                profile.reset_failed_attempts()
                login(self.request, authenticated_user)
                messages.success(self.request, f"Successfully logged in as {username}.")
                return redirect(self.get_success_url())
            else:
                # Invalid password, increment failed attempts
                profile.increment_failed_attempts()
                profile.save()  # Make sure to save changes to the profile!
                messages.error(
                    self.request,
                    f"Invalid password. Attempt {profile.failed_attempts} of 3.",
                )
                return self.form_invalid(form)

        else:
            # Handle invalid form case (form was not filled out correctly)
            username = form.cleaned_data.get("username")

            if username:
                user = User.objects.filter(username=username).first()
                if user:
                    profile, created = UserLoginAttempt.objects.get_or_create(user=user)
                    if profile.is_locked_out():
                        remaining_time = profile.lockout_until - timezone.now()
                        total_seconds = int(remaining_time.total_seconds())
                        minutes, seconds = divmod(total_seconds, 60)
                        messages.error(
                            self.request,
                            f"Account is locked. Try again in {int(minutes)} minutes and {int(seconds)} seconds.",
                        )
                    else:
                        profile.increment_failed_attempts()
                        messages.error(
                            self.request,
                            f"Login failed. Attempt {profile.failed_attempts} of 3.",
                        )
                else:
                    messages.error(self.request, "Username does not exist.")
            else:
                messages.error(
                    self.request,
                    "Login failed. Please check your username and password.",
                )

            return self.form_invalid(form)


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
        messages.success(request, "You have successfully logged out.")
        return super().post(request, *args, **kwargs)


def logout_confirm(request):
    return render(request, "registration/logout_confirm.html")


# [x] make encryption logic in javascript to take input
