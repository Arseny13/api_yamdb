from random import choice
from string import ascii_lowercase, digits

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .pagination import UserPagination

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title

from users.models import User
from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer,
    TokenSerializer,
    SignUpSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializerCreate,
    TitleSerializer, UserSerializer
)


CONFIRMATION_CODE_CHARS = tuple(ascii_lowercase + digits)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        """Получение текущего объекта произведения (title)."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получение выборки с отзывами текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва для текущего произведения."""
        serializer.save(
            author=self.request.user,
            title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsReadOnly,)
    pagination_class = PageNumberPagination

    def get_review(self):
        """Получение текущего объекта отзыва (review)."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получение выборки с комментариями текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создание комментария для текущего отзыва."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class APIUser(APIView):
    """Класс для переопределения запросов GET и PATCH"""
    pagination_class = UserPagination

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserViewSet(viewsets.ModelViewSet):
    """Класс UserViewSet для User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    pagination_class = PageNumberPagination


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    """Отправляет код подтверждения на e-mail."""
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    if serializer.is_valid():
        cc_lst = []
        for number_of_symbols in range(16):
            cc_lst.append(choice(CONFIRMATION_CODE_CHARS))
        confirmation_code = ''.join(cc_lst)
        User.objects.get_or_create(
            username=username,
            email=email
        )
        User.objects.filter(username=username, email=email).update(

            confirmation_code=make_password(
                confirmation_code, salt=None, hasher='default'
            )
        )
        mail_subject = 'Код подтверждения на Yamdb.ru'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>', [email])
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получает JWT-токен"""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(
            User, username=username,
        )
        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_201_CREATED
            )
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    """Класс ModelViewSet для Post."""
    queryset = Title.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if (
            self.action == 'create'
            or self.action == 'update'
            or self.action == 'partial_update'
        ):
            return TitleSerializerCreate
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Класс CreateListDestroyViewSetдля Category."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class GenreViewSet(CreateListDestroyViewSet):
    """Класс ModelViewSet для Genre."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
