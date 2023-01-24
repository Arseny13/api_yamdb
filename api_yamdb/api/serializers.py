from rest_framework import serializers

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

