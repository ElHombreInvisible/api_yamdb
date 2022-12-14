from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)
    # description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50,
                            unique=True)
    # description = models.TextField()

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='titles',
        blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, on_delete=models.PROTECT,
        related_name='titles',
        through='GenresOfTitle')
    # rating = 

    def __str__(self):
        return self.name


class GenresOfTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) # или Protect?
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

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
    score = models.IntegerField(default=1, db_index=True,
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ]
                                )

    def __str__(self):
        return self.text

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)