from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def register_errors_view(request):
    message = {}

    try:
        validate_email(request.POST["email"])
    except ValidationError:
        message['email'] = "Некоректний email"

    if User.objects.filter(username=request.POST["username"]).exists():
        message['username'] = "Користувач з таким ім'ям вже існує"

    if request.POST["password"] != request.POST["password2"]:
        message['password2'] = "Паролі не співпадають"
    return message


def register_view(request):
    if request.method == "GET":
        return render(request, "authorization/register.html")
    if request.method == "POST":
        message = register_errors_view(request)

        if message:
            return render(request, "authorization/register.html", {"message": message})

        user = User.objects.create_user(
            username=request.POST["username"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            password=request.POST["password"],
            email=request.POST["email"],
        )
        login(request, user)
        return redirect("shop:index")
    return HttpResponse(status=405)


def login_view(request):
    if request.method == "GET":
        return render(request, "authorization/login.html")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("shop:index")
        elif not User.objects.filter(username=request.POST["username"]).exists():
            return render(
                request,
                "authorization/login.html",
                {"message": {"username": "Невірне ім'я користувача"}},
            )
        else:
            return render(
                request,
                "authorization/login.html",
                {"message": {"password": "Невірний пароль"}}
            )
    return HttpResponse(status=405)


def logout_view(request):
    logout(request)
    return redirect("shop:index")

