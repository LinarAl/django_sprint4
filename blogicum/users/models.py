"""Кастомная модель пользователя"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """Переопределена стандартная модель. Есть возможность изменять ее в
    будущем"""
    pass
