from django.shortcuts import render, redirect
from django.contrib import messages
from authenticate.models import BankUser
from django.db import connection

from .forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        with connection.cursor() as cursor:
            cursor.executescript(
                f"SELECT * FROM authenticate_bankuser WHERE username == '{request.POST['username']}';"
            )
            for user in cursor.fetchone():
                if request.POST["username"] == user.username:
                    return render(request, "authenticate/signup.html", {"form": form})

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "You can now login to your account"
            )
            return redirect("authenticate:login")

    else:
        form = UserCreationForm()
    return render(request, "authenticate/signup.html", {"form": form})
