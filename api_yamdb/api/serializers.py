from rest_framework import serializers
from reviews.models import Title, Category, Genre

from users.models import User


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
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        """Класс мета для модели Genre."""
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        """Класс мета для модели Title."""
        model = Title
        fields = ('name', 'category', 'genre', 'year')

