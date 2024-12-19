"""Переадресация запросов
Импорты: функций path и views. В urlpatterns указываюся какие запросы
переадресовываются во views функции. Для удобства каждому URL указывается имя
name, которое будет использовано в ссылках html шаблонов. Так же указано
пространство имен app_name, чтобы определять к какому приложению относится
name.

<int:id> - означает что id целое число; пример запроса: posts/2/

<slug:category_slug> - означает что category_slug состоит из простых символов и
цифор; пример запроса: posts/some-t-1/.
"""


from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]
