from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from .validator import username_value_not_me

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUserManager(BaseUserManager):
    """Класс для создания обычного пользователя/суперпользователя."""

    def create_superuser(self, email, password, **kwargs):
        """
        Cоздает и сохраняет суперпользователя
        с указанным адресом электронной почты и паролем.
        """
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.is_admin = True
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        """
        Cоздает и сохраняет пользователя
        с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('У пользователя должен быть e-mail')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    """Класс для создания модели пользователя."""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Ник пользователя',
        max_length=150,
        unique=True,
        validators=[username_value_not_me]
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=15,
        null=True
    )
    role = models.CharField(
        'Кем является',
        choices=CHOICES,
        max_length=15,
        default='user'
    )

    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return str(self.username)
