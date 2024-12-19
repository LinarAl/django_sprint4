"""Обработка запросов
Импорт функции render. Две функции обрабатывают запросы: about - страница с
информацией о проекте, rules - страница правилами для пользователей.
"""
from django.shortcuts import render

# Create your views here.


def about(request):
    """Обработка страницы с информацией о проекте.
    template - шаблон страницы html; Функция возвращает
    вызов функции render с параметрами(request, template).
    """
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Обработка страницы с правилами для пользователей.
    template - шаблон страницы html; Функция возвращает
    вызов функции render с параметрами(request, template).
    """
    template = 'pages/rules.html'
    return render(request, template)
