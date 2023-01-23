from django.db import models


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
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
