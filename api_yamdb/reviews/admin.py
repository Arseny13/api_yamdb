from django.contrib import admin

from .models import Title, Category, Genre


class TitleInline(admin.TabularInline):
    model = Title.genre.through
    extra = 3


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',)
    inlines = (
        TitleInline,
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
