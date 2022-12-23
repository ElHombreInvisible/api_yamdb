from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title

from .validators import validate_year


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
        return int(obj.rating) if obj.rating is not None else None

    def validate_year(self, data):
        return validate_year(data)


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
        return validate_year(data)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    title = SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('title',)
        model = Review


class CreateReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'score',)
        model = Review

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        if (self.context['request'].method == 'POST'
           and Review.objects.filter(author=author, title=title_id).exists()):
            raise serializers.ValidationError('Вы уже оставляли отзыв '
                                              'к данному '
                                              'произведению.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
