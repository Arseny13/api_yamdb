
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение',
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_title_author"
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]

class Genre(models.Model):
    """Класс жанра"""
    name = models.CharField(
        max_length=256,
        verbose_name='name жанра',
        help_text='Введите имя жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug жанра',
        help_text='Введите слаг жанра',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        """Класс Meta для Genres описание метаданных."""
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class Category(models.Model):
    """Класс категории"""
    name = models.CharField(
        max_length=200,
        verbose_name='name категории',
        help_text='Введите имя категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug категории',
        help_text='Введите слаг категории',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        """Класс Meta для Categories описание метаданных."""
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Title(models.Model):
    """Класс произведения"""
    name = models.CharField(
        max_length=200,
        verbose_name='Name произведения',
        help_text='Введите имя произведения',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться тайтл',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
    )
    year = models.IntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Класс связи жанра и произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
