from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer)
from reviews.models import Title, Category, Genre


class TitleViewSet(viewsets.ModelViewSet):
    """Класс ModelViewSet для Post."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """Класс ModelViewSet для Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    """Класс ModelViewSet для Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
