from django.contrib import admin

from .models import Category, Genre, GenresOfTitle, Title
from .models import Review, Comment

class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'name', 'category', 'genres', 'rating')
    search_fields = ('name',)
    list_filter = ('year', 'category',)
    empty_value_display = '-пусто-'

    def genres(self, name):
        queryset = GenresOfTitle.objects.filter(title=name)
        genres = []
        for elem in queryset:
            genres.append(elem.genre)
        return genres

    def rating(self, name):
        queryset = Review.objects.filter(title=name)
        rating=[]
        for elem in queryset:
            rating.append(elem.score)
        return int(sum(rating)/len(rating))

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
admin.site.register(GenresOfTitle)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
