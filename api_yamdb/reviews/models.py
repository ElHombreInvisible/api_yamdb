from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
    category = models.ManyToManyField(
        Category, on_delete=models.CASCADE,
        through='CategoriesOfTitle')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        blank=True, null=True)
    # rating = 

    def __str__(self):
        return self.name


class CategoriesOfTitle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} категория:{self.category}'
