from django import forms
from django.core.exceptions import ValidationError

from .models import TransferToConfirm


class NewTransferForm(forms.ModelForm):
    class Meta:
        model = TransferToConfirm
        fields = ("title", "recipient", "date", "amount", "iban")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class AuthCodeValidator:
    auth_code = ""
    message = "Wrong Authorisation Code."
    code = "invalid"

    def __init__(self, auth_code=None, message=None, code=None):
        if auth_code is not None:
            self.auth_code = auth_code
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if value != self.auth_code:
            raise ValidationError(self.message, code=self.code, params={"value": value})


class ConfirmTransferForm(forms.Form):
    def __init__(self, auth_code, *args, **kwargs):
        super(ConfirmTransferForm, self).__init__(*args, **kwargs)
        self.fields["auth_code"] = forms.CharField(
            required=False,
            min_length=6,
            max_length=6,
            validators=[AuthCodeValidator(auth_code)],
        )
