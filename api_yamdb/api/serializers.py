from rest_framework import serializers

from reviews.models import Title, Category, Genre


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
