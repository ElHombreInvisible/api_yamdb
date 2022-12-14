# api_yamdb/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ACCESS_LEVEL = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    access_level = models.CharField(choices=ACCESS_LEVEL,
                                    default='user',
                                    max_length=13)
