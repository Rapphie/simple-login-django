import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib import messages
from .forms import SignUpForm
from .models import User


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = User.objects.create(
                name=name, username=username, email=email, password=password
            )
            user.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            else:
                messages.success(request, "Account created successfully!")
                return redirect("sign_in")
        else:
            errors = list(form.errors.values())
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": errors})
    else:
        form = SignUpForm()

    return render(request, "sign_in.html", {"form": form})


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print("Printing token...")
    token = request.POST["credential"]

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ["GOOGLE_OAUTH_CLIENT_ID"]
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session["user_data"] = user_data

    return redirect("portfolio")


# def auth_login(request):


def sign_out(request):
    del request.session["user_data"]
    return redirect("sign_in")


def portfolio(request):
    return render(request, "portfolio.html")


def sign(request):
    return render(request, "sign.html")


# def isPasswordMatch:
