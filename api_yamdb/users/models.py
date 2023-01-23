from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """Класс для создания обычного пользователя/суперпользователя."""

    def create_superuser(self, email, password, **kwargs):
        """Создает суперпользователя."""
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        """Создает обычного пользователя."""
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user



class User(AbstractUser):
    """Класс для создания модели пользователя."""

    __CHOICES = (
        ('user','Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        default='code_is_missing'
    )
    role = models.CharField(
        'Кем является',
        max_length=9,
        choices=__CHOICES,
        default='user'
    )
    objects = CustomUserManager()