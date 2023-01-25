from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

import datetime as dt


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title',),
                message='Повторный отзыв!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    class Meta:
        model = User
        fields = '__all__'


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для кода подтверждения."""
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


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
        fields = ('id', 'name', 'description', 'category', 'genre', 'year')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        """Класс мета для модели Title."""
        model = Title

        fields = ('id', 'name', 'description', 'category', 'genre', 'year')

