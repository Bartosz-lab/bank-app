from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserCreationForm


def index(request):
    return render(request, "user_profile/index.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            return redirect("user_profile:index")

    else:
        form = UserCreationForm()
    return render(request, "authenticate/signup.html", {"form": form})
