"""Обработка запросов статичных страниц about и rules
about - страница с информацией о проекте, rules - страница правилами для
пользователей.
"""

from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """Обработка страницы с информацией о проекте."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Обработка страницы с правилами для пользователей."""

    template_name = 'pages/rules.html'
