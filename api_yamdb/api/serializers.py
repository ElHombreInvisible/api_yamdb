import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        # rating = None
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return int(rating) if rating is not None else None

    def validate_year(self, data):
        # if self.context['request'].year > dt.datetime.now().year:
        if data > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Неверная дата выхода или произведение еще не вышло.')
        return data

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError('name должен быть не'
                                              ' более 256 символов')
        return value


class CreateTitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(required=True, slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(many=True, required=True,
                             queryset=Genre.objects.all(), slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def validate_year(self, data):
        # if self.context['request'].year > dt.datetime.now().year:
        if data > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Неверная дата выхода или произведение еще не вышло.')
        return data

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError('name должен быть не'
                                              ' более 256 символов')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    title = SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('title',)
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author', 'title'),
        #         message='Можно оставлять только один отзыв к произведению'
        #     )
        # ]


class CreateReviewSerializer(serializers.ModelSerializer):
    #    author = serializers.SlugRelatedField(
    #        read_only=True, slug_field='username',
    #        default=serializers.CurrentUserDefault())
    #    title = SlugRelatedField(read_only=True, slug_field='title')
    class Meta:
        fields = ('id', 'text', 'score',)
    #        read_only_fields = ('author','title',)
        model = Review

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(f'Вы уже оставляли отзыв '
                                              f'к данному '
                                              f'произведению - {title.name}. '
                                              f'с id {title.id}')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')  # , 'review'
        # read_only_fields = ('review',)
        model = Comment
