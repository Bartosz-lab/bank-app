from django.contrib import admin

from .models import Transfer, TransferToConfirm


class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Transfer)
class TransferAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ["title", "date", "amount", "user"]
    ordering = ["-date", "pk"]


@admin.register(TransferToConfirm)
class TransferToConfirmAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ["title", "date", "amount", "user", "created"]
    ordering = ["-created", "pk"]
    fields = ["title", "recipient", "date", "amount", "iban", "user", "created"]

    def has_delete_permission(self, request, obj=None):
        return admin.ModelAdmin.has_delete_permission(self, request, obj=None)
