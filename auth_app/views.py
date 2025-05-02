from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("shop:index")

        return render(request, "authorization/register.html", {"form": form})
    else:
        form = RegisterForm()
    return render(request, "authorization/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            if user:
                login(request, user)
                return redirect("shop:index")
        else:
            return render(request, "authorization/login.html", {"form": form})

    else:
        form = LoginForm()
    return render(request, "authorization/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("shop:index")
