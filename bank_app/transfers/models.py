from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    RegexValidator,
    DecimalValidator,
    MinValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)


class BaseTransfer(models.Model):
    title = models.CharField(
        max_length=50, validators=[MinLengthValidator(5), MaxLengthValidator(50)]
    )
    recipient = models.CharField(
        max_length=50, validators=[MinLengthValidator(5), MaxLengthValidator(50)]
    )
    date = models.DateField()
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        validators=[
            MinValueValidator(0.01),
            DecimalValidator(max_digits=20, decimal_places=2),
        ],
    )
    iban = models.CharField(
        max_length=26,
        help_text="BANK Account Number",
        validators=[RegexValidator("\d{26}$")],
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Transfer(BaseTransfer):
    pass


class TransferToConfirm(BaseTransfer):
    auth_code = models.CharField(
        max_length=6,
        help_text="Authorisation Code",
        validators=[RegexValidator("\d{6}$")],
    )
    created = models.DateTimeField(auto_now=True)
