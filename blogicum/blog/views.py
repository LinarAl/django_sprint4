"""Обработка запросов.
Импорты datetime, функции render и get_object_or_404, моделей Post и Category.
Три функции обрабатывают запросы: index - страница с постами,
post_detail - страница с информацией о конкретном посте,
category_posts - страница с категорией постов.
"""
from django.db.models import Count

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from django.shortcuts import get_object_or_404, redirect
from blog.models import Post, Category, Comment
from .utils import sql_filters
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.urls import reverse


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


@login_required
def add_comment(request, post_id):
    """Создание комментрария.
    Отображается на странице PostDetailView
    """
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    post = get_object_or_404(Post, pk=post_id)
    # Функция должна обрабатывать только POST-запросы.
    form = CommentForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        comment = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        comment.author = request.user
        # В поле birthday передаём объект дня рождения.
        comment.post = post
        # Сохраняем объект в БД.
        comment.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('blog:post_detail', post_id=post_id)


class EditComment(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class DeleteComment(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostListView(ListView):
    """Cтраница с постами."""

    paginate_by = 10
    ordering = '-pub_date', 'title'
    model = Post
    template_name = 'blog/index.html'
    # context_object_name = 'page_obj'

    def get_queryset(self):

        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author',)).annotate(
                comment_count=Count("comments"))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context['paginator'].page(1).object_list)
    # #         'category', 'author', 'location',)
    # #     paginator = Paginator(posts, 10)
    # #     page_number = self.request.GET.get('page')
    # #     page_obj = paginator.get_page(page_number)
    # #     context['page_obj'] = page_obj
    #     return context


class PostDetailView(DetailView):
    """Cтраница с информацией о конкретном посте."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        author = False
        if Post.objects.filter(
            id=self.kwargs['post_id'], author=self.request.user.id
        ):
            author = True
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(id=self.kwargs['post_id']), author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Записываем в переменную form пустой объект формы.
        context['form'] = CommentForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['comments'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.comments.select_related(
                'author')
        )
        return context


class CategoryPostsView(ListView):
    """Cтраница с постами по категории."""

    paginate_by = 10
    ordering = '-pub_date', 'title'
    model = Post
    template_name = 'blog/category.html'
    # context_object_name = 'page_obj'

    def get_queryset(self):
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(category__slug=self.kwargs['category_slug'])).annotate(comment_count=Count("comments"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(
            slug=self.kwargs['category_slug'],
            is_published=True
        )

        context['category'] = category
        return context


class ProfileView(ListView):
    """Страница профиля пользователя."""

    paginate_by = 10
    ordering = '-pub_date', 'title'
    model = Post
    template_name = 'blog/profile.html'
    # context_object_name = 'page_obj'

    def get_queryset(self):
        """Запрос к бд с фильрами.
        Если пользователь и автор профиля страницы совпадают, то пользователь
        может просматривать неопубликованные посты.
        """
        author = False
        if str(self.kwargs['username']) == str(self.request.user):
            author = True
        return sql_filters(Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(author__username=self.kwargs['username']).annotate(
            comment_count=Count("comments")), author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = User.objects.get(username=self.kwargs['username'])
        context['profile'] = profile
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Страница создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Страница редактирования поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Страница удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
