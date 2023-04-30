from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    MaxLengthValidator,
    MinLengthValidator,
)


class BankUserManager(BaseUserManager):
    def create_user(self, username, email, phone, password=None):
        """
        Creates and saves a User with the given username, email, phone and password.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone, password=None):
        """
        Creates and saves a superuser with the given username, email, phone and password.
        """
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BankUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[MinLengthValidator(5), MaxLengthValidator(30)],
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        validators=[EmailValidator],
    )
    phone = models.CharField(
        max_length=12,
        help_text="Contact phone number",
        validators=[
            RegexValidator("^(\+48)?\d{9}$", message="Enter a valid phone number.")
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BankUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    def __str__(self):
        return self.username
