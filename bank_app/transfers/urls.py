from django.urls import path

from . import views

app_name = "transfers"
urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("new/", views.CreateView.as_view(), name="new"),
    path("confirm/<int:confirm_id>", views.ConfirmView.as_view(), name="confirm"),
    path("reject/<int:reject_id>", views.RejectView.as_view(), name="reject"),
    path("<int:pk>", views.DetailView.as_view(), name="details"),
]
