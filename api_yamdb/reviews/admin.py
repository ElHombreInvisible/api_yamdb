from django.contrib import admin

from .models import Category, Genre, GenresOfTitle, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'name', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenresOfTitle)
