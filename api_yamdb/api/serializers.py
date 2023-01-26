import datetime as dt
import re

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICES, User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        """Проверка на повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        user = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if user.reviews.filter(title_id=title_id).exists():
            raise serializers.ValidationError('Повторный отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name', 'bio'
        )

    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, value):
            raise serializers.ValidationError('Проверьте username!')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)
    role = serializers.ChoiceField(choices=CHOICES, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'first_name', 'last_name', 'bio'
        )

    def validate(self, data):
        """Проверка на повторные email."""
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    'Уже username  c данной почтой существует!'
                )
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError('Уже существует!')
        return data

    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, value):
            raise serializers.ValidationError('Проверьте username!')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистариции."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        fields = ('username', 'email')

    def validate(self, data):
        """Проверка на повторные email."""
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    'Уже username  c данной почтой существует!'
                )
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError('Уже существует!')
        return data

    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, value):
            raise serializers.ValidationError('Проверьте username!')
        if value == 'me':
            raise serializers.ValidationError('Me запрещено')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        """Класс мета для модели Category."""
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        """Класс мета для модели Genre."""
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор при создании для модели Title."""
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug')

    class Meta:
        """Класс мета для модели Title."""
        model = Title
        fields = ('id', 'name', 'description', 'category', 'genre', 'year',)

    def validate_year(self, value):
        """Валидация для года выпуска."""
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год выпуска!')
        if value < 0:
            raise serializers.ValidationError('Год выпуска с минусом!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        """Класс мета для модели Title."""
        fields = ('id', 'name', 'description', 'category', 'genre', 'year',
                  'rating')
        model = Title

    def get_rating(self, obj):
        """Валидация для рейтитнга."""
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return rating
