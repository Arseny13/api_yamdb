from rest_framework import viewsets, mixins


class CreateListDestroyViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс ViewSet только для создания и полученияИ и удаления объектов."""
    pass
