from django import forms
from django.core.exceptions import ValidationError

from .models import TransferToConfirm


class NewTransferForm(forms.ModelForm):
    class Meta:
        model = TransferToConfirm
        fields = ("title", "recipient", "date", "amount", "iban")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class ConfirmTransferForm(forms.Form):
    auth_code = forms.CharField(required=False, min_length=6, max_length=6)

    def __init__(self, confirm_id, *args, **kwargs):
        self.confirm_id = confirm_id
        super(ConfirmTransferForm, self).__init__(*args, **kwargs)

    def clean_auth_code(self):
        auth_code = self.cleaned_data.get("auth_code")
        try:
            transfer = TransferToConfirm.objects.get(pk=self.confirm_id)
        except:
            raise ValidationError("Time Left")
        else:
            if auth_code != transfer.auth_code:
                raise ValidationError("Wrong Authorisation Code")

        return auth_code
