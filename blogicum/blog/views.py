"""Обработка запросов.
Импорты datetime, функции render и get_object_or_404, моделей Post и Category.
Три функции обрабатывают запросы: index - страница с постами,
post_detail - страница с информацией о конкретном посте,
category_posts - страница с категорией постов.
"""


from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from .utils import sql_filters
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


# def index(request):
#     """Обработка страницы с постами."""
#     template = 'blog/index2.html'
#     post_list = sql_filters(Post.objects.select_related(
#         'category', 'location', 'author')).order_by('-pub_date', 'title')[:5]
#     context = {'page_obj': post_list}
#     return render(request, template, context)


class PostListView(ListView):
    """Cтраница с постами."""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     posts = Post.published().select_related(
    #         'category', 'author', 'location',)
    #     paginator = Paginator(posts, 10)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     context['page_obj'] = page_obj
    #     return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     posts = Post.objects.select_related(
    #         'category', 'author', 'location',)
    #     paginator = Paginator(posts, 10)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     context['page_obj'] = page_obj
    #     return context


# def post_detail(request, id):
#     """Обработка страницы с информацией о конкретном о посте."""
#     template = 'blog/detail.html'
#     post = get_object_or_404(
#         sql_filters(Post.objects.select_related(
#             'category', 'location', 'author')),
#         id=id
#     )
#     context = {'post': post}
#     return render(request, template, context)


class PostDetailView(DetailView):
    """Cтраница с информацией о конкретном посте."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(id=self.kwargs['id']))


# def category_posts(request, category_slug):
#     """Обработка страницы с категорией постов."""
#     template = 'blog/category.html'
#     category = get_object_or_404(
#         Category,
#         slug=category_slug,
#         is_published=True
#     )
#     post_list = sql_filters(
#         category.posts.select_related('location', 'author')
#     ).order_by('-pub_date', 'title')

#     context = {'category': category, 'post_list': post_list}
#     return render(request, template, context)


class CategoryPostsView(ListView):
    """Cтраница с постами по категории."""

    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(category__slug=self.kwargs['category_slug']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(
            slug=self.kwargs['category_slug'],
            is_published=True
        )

        context['category'] = category
        return context


# def profile(request, username):
#     """Обработка страницы профиля пользователя."""
#     template = 'blog/profile.html'
#     profile = get_object_or_404(
#         User,
#         username=username
#     )
#     post_list = sql_filters(Post.objects.select_related(
#         'category', 'location', 'author')).filter(
#             author=User.objects.get(username=username)
#     )
#     context = {'profile': profile, 'page_obj': post_list}
#     return render(request, template, context)


class ProfileView(ListView):
    """Страница профиля пользователя."""

    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(author__username=self.kwargs['username']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = User.objects.get(username=self.kwargs['username'])
        print(profile)

        context['profile'] = profile
        return context


class PostCreateView(CreateView):
    """Страница создания поста."""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

# class EditProfile(UpdateView):
#     """Обработка страницы редактирования профиля пользователя."""

#     model = User,
#     template_name = 'blog/user.html',
#     form_class = CustomUserChangeForm,
#     success_url = reverse_lazy('blog:index')
