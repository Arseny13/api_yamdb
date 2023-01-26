from django.contrib import admin

from reviews.models import Category, Genre, Title


class TitleInline(admin.TabularInline):
    model = Title.genre.through
    extra = 3


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',)
    inlines = (
        TitleInline,
    )


admin.site.register(Category)
admin.site.register(Genre)
