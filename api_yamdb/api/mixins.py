from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для создания и получения и удаления объектов."""
    pass
