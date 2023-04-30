from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = "authenticate"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="authenticate/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="authenticate/password_change.html",
            success_url=reverse_lazy("authenticate:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authenticate/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path("signup/", views.signup, name="signup"),
]


# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
