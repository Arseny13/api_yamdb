from django.contrib import admin

from .models import Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
