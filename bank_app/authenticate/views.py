from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "You can now login to your account"
            )
            return redirect("authenticate:login")

    else:
        form = UserCreationForm()
    return render(request, "authenticate/signup.html", {"form": form})
