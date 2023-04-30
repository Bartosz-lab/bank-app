from django.contrib.auth import get_user_model
from django.test import TestCase


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
        self.assertFalse(user.is_admin)

    def test_create_user_no_username(self):
        User = get_user_model()
        with self.assertRaisesMessage(ValueError, "Users must have an username"):
            User.objects.create_user(
                username="", email="tester1@user.com", phone="123456789", password="foo"
            )

    def test_create_user_no_email(self):
        User = get_user_model()
        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            User.objects.create_user(
                username="tester", email="", phone="123456789", password="foo"
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
        self.assertTrue(admin_user.is_admin)
