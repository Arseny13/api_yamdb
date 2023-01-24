from reviews.models import Title

import django_filters


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug',
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')
