from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Создает админ-зону с понятным интерфейсом."""
    list_display = (
        "pk",
        "email",
        "bio",
        "confirmation_code",
        "role"
    )
    list_editable = ('role',)
    search_fields = ('role',)
    list_filter = ('role', )
    empty_value_display = '-пусто-'
