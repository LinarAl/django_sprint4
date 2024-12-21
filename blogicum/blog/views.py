"""Обработка запросов.
Импорты datetime, функции render и get_object_or_404, моделей Post и Category.
Три функции обрабатывают запросы: index - страница с постами,
post_detail - страница с информацией о конкретном посте,
category_posts - страница с категорией постов.
"""


from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from .utils import sql_filters
from django.contrib.auth import get_user_model

from django.views.generic.edit import UpdateView, CreateView
from users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin

User = get_user_model()


def index(request):
    """Обработка страницы с постами."""
    template = 'blog/index.html'
    post_list = sql_filters(Post.objects.select_related(
        'category', 'location', 'author')).order_by('-pub_date', 'title')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    """Обработка страницы с информацией о конкретном о посте."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        sql_filters(Post.objects.select_related(
            'category', 'location', 'author')),
        id=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Обработка страницы с категорией постов."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = sql_filters(
        category.posts.select_related('location', 'author')
    ).order_by('-pub_date', 'title')
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)


def profile(request, username):
    """Обработка страницы профиль пользователя."""
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username
    )
    context = {'profile': profile}
    return render(request, template, context)


# class EditProfile(UpdateView):
#     """Обработка страницы редактирования профиля пользователя."""

#     model = User,
#     template_name = 'blog/user.html',
#     form_class = CustomUserChangeForm,
#     success_url = reverse_lazy('blog:index')
