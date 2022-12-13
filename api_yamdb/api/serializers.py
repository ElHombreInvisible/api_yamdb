import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')

class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(read_only=True)
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
