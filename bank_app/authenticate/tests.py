from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpRequest

from .forms import UserCreationForm


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="tester1",
            email="tester1@user.com",
            phone="123456789",
            password="foo",
        )
        self.assertEqual(user.username, "tester1")
        self.assertEqual(user.email, "tester1@user.com")
        self.assertEqual(user.phone, "123456789")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_username(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="", email="tester1@user.com", phone="123456789", password="foo"
            )

    def test_create_user_no_email(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="tester", email="", phone="123456789", password="foo"
            )

    def test_create_user_no_phone(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="tester",
                email="tester@user.com",
                phone="",
                password="foo",
            )

    def test_create_user_no_all_fields(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="tester",
                email="tester@user.com",
                password="foo",
            )

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superuser",
            email="superuser@user.com",
            phone="123456789",
            password="foo",
        )
        self.assertEqual(admin_user.username, "superuser")
        self.assertEqual(admin_user.email, "superuser@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserCreationFormTest(TestCase):
    def test_valid_user(self):
        response = self.client.post(
            "/auth/signup",
            data={
                "username": "tester1",
                "email": "tester1@example.com",
                "phone": "123456789",
                "password1": "Password1@",
                "password2": "Password1@",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)

    def test_phone_validator(self):
        request = HttpRequest()
        request.POST = {
            "username": "tester1",
            "email": "tester1@example.com",
            "phone": "123 456 78",
            "password1": "Password1@",
            "password2": "Password1@",
        }
        form = UserCreationForm(request.POST)
        self.assertFormError(
            form=form, field="phone", errors=["Enter a valid phone number."]
        )

    def test_phone_validator2(self):
        request = HttpRequest()
        request.POST = {
            "username": "tester1",
            "email": "tester1@example.com",
            "phone": "+48123456789",
            "password1": "Password1@",
            "password2": "Password1@",
        }
        form = UserCreationForm(request.POST)
        self.assertFormError(form=form, field=None, errors=[])
