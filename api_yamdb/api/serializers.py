# api/serializers
import re
import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(read_only=True, slug_field='slug')
    '''genre = SlugRelatedField(read_only=True,
                             many = True,
                             queryset = Genre.objects.all(),
                             read_only=True)'''
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
    
    def get_rating(self, obj):
        return None

    def validate(self, data):
        # if self.context['request'].year > dt.datetime.now().year:
        if data['year'] > dt.datetime.now().year:
            raise serializers.ValidationError(
            'Неверная дата выхода или произведение еще не вышло.')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Можно оставлять только один отзыв к произведению'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
