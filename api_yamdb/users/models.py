# api_yamdb/users/models.py
import random

from django.contrib.auth.models import AbstractUser
from django.db import models

# from api.validators import validate_username

ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        # validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=True,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE,
        default='user',
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        # null=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default=''.join(map(str, random.sample(range(10), 6)))
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
