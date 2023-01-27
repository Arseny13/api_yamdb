from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnly(BasePermission):
    """Перминш для моделей Review, Comment."""
    def has_permission(self, request, view):
        """GET-запрос не требует авторизации."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Пользователь User не может редактировать чужой пост."""
        return (
            (request.method == 'PATCH' or request.method == 'DELETE')
            and request.user.role == 'user'
        ) and obj.author == request.user


class IsAdmin(BasePermission):
    """Перминш для Админа."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'


class IsAdminOrReadOnly(BasePermission):
    """Перминш для Админа и разрешено чтение."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
