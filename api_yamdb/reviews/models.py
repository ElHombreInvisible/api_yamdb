from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='titles',
        blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenresOfTitle')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-year', ]


class GenresOfTitle(models.Model):

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='titles_of_genre')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='title_genres')

    def __str__(self):
        return f'{self.title} категория:{self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(db_index=True, blank=False, null=False,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ]
                                )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date', ]

        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='UniqueReviewCOnstraint')
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date', ]
