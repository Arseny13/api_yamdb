from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validator import username_value_not_me

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUserManager(BaseUserManager):
    """Класс для создания обычного пользователя/суперпользователя."""

    def create_superuser(self, username, email, password, **kwargs):
        """
        Cоздает и сохраняет суперпользователя
        с указанным адресом электронной почты и паролем.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )

    def create_user(self, username, email, password=None, **kwargs):
        """
        Cоздает и сохраняет пользователя
        с указанным адресом электронной почты и паролем.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        if password is None:
            user.set_unusable_password()
        else:
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
        validators=(username_value_not_me,)
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
        max_length=100,
        null=True
    )
    role = models.CharField(
        'Кем является',
        choices=CHOICES,
        max_length=15,
        default=USER,
    )

    objects = CustomUserManager()

    REQUIRED_FIELDS = ('email',)
    USERNAME_FIELDS = 'email'

    @property
    def is_user(self):
        """Проверяет, если пользователь Юзер."""
        return self.role == USER

    @property
    def is_admin(self):
        """Проверяет, если пользователь Администратор."""
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверяет, если пользователь Модератор."""
        return self.role == MODERATOR or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
