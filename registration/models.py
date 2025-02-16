from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Пользователь должен указать имя пользователя.")
        username = self.model.normalize_username(username)
        extra_fields.setdefault("coins", 1000)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("coins", 1000)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        user = self.create_user(username, password, **extra_fields)
        return user


class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("username", unique=True, max_length=150, db_index=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    coins = models.PositiveIntegerField(
        default=1000, help_text="User's coin balance.", db_index=True
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Авторизационник"
        verbose_name_plural = "Авторизационники"
        abstract = True


class CustomUser(CustomAbstractUser):
    class Meta(CustomAbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
