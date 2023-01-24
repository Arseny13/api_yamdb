from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from reviews.models import Comment, Review, Title
# from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer,
                          ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

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
    """Вюсет модели комментариев."""
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        """Получение текущего объекта отзыва (review)."""
        return get_object_or_404(Title, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получение выборки с комментариями текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создание комментария для текущего отзыва."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
