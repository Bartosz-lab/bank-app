from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime, timedelta

from .forms import NewTransferForm, ConfirmTransferForm

User = get_user_model()


class NewTransferFormTest(TestCase):
    def test_validators(self):
        POST = {
            "title": "Transfer1",
            "recipient": "tester1",
            "date": datetime.today(),
            "amount": "123.45",
            "iban": "11222233334444555566667777",
        }
        form = NewTransferForm(POST)
        self.assertTrue(form.is_valid())

    def test_amount_validator(self):
        POST = {
            "title": "Transfer1",
            "recipient": "tester1",
            "date": datetime.today(),
            "amount": "123.456",
            "iban": "11222233334444555566667777",
        }
        form = NewTransferForm(POST)
        self.assertFormError(
            form=form,
            field="amount",
            errors=["Ensure that there are no more than 2 decimal places."],
        )

        POST["amount"] = "ab.11"
        form = NewTransferForm(POST)
        self.assertFormError(
            form=form,
            field="amount",
            errors=["Enter a number."],
        )

    def test_date_validator(self):
        POST = {
            "title": "Transfer1",
            "recipient": "tester1",
            "date": datetime.today() - timedelta(days=1),
            "amount": "123.45",
            "iban": "11222233334444555566667777",
        }
        form = NewTransferForm(POST)
        self.assertFormError(
            form=form,
            field="date",
            errors=["The date cannot be in the past!"],
        )

        POST["date"] = datetime.today() - timedelta(days=10)
        form = NewTransferForm(POST)
        self.assertFormError(
            form=form,
            field="date",
            errors=["The date cannot be in the past!"],
        )
        POST["date"] = datetime.today() + timedelta(days=370)
        form = NewTransferForm(POST)
        self.assertFormError(
            form=form,
            field="date",
            errors=["The date cannot be later then 365 days from now!"],
        )


class ConfirmTransferFormTest(TestCase):
    def test_auth_code_ok(self):
        POST = {"auth_code": "123456"}
        form = ConfirmTransferForm("123456", POST)
        self.assertFormError(
            form=form,
            field="auth_code",
            errors=[],
        )

    def test_auth_code_wrong(self):
        POST = {"auth_code": "111111"}
        form = ConfirmTransferForm("123456", POST)
        self.assertFormError(
            form=form,
            field="auth_code",
            errors=["Wrong Authorisation Code."],
        )

    def test_auth_code_bad(self):
        POST = {"auth_code": "123"}
        form = ConfirmTransferForm("123456", POST)
        self.assertFormError(
            form=form,
            field="auth_code",
            errors=[
                "Wrong Authorisation Code.",
                "Ensure this value has at least 6 characters (it has 3).",
            ],
        )
