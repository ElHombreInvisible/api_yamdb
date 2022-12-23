from django.contrib import admin
from django.db.models import Avg

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'name', 'category', 'rating')
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'

    def rating(self, name):
        rating = None
        title = Title.objects.get(name=name)
        rating = title.reviews.aggregate(Avg('score')).get('score__avg')
        return rating


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'review', 'pub_date')
    list_filter = ('pub_date',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
