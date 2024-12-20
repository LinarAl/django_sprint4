"""Кастомная модель пользователя"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.db import models

User = get_user_model()


class MyUser(AbstractUser):
    """Переопределена стандартная модель. Есть возможность изменять ее в
    будущем"""
    pass


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для создания пользователя.
    Наследуется от стандартной формы, изменяет модель пользователя на
    кастомную.
    """

    class Meta:
        model = User
        fields = ("username",)
