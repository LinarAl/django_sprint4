"""Дополнительные функции"""
from datetime import datetime


def sql_filters(sql_req, author=False):
    """Фильтры для SQL запроса.
    Фильтры не применяются для автора поста.
    """
    if not author:
        return sql_req.filter(
            is_published=True,
            pub_date__time__lt=datetime.now(),
            # pub_date__date__lt=now,
            # pub_date__time__lt=now,
            category__is_published=True
        )
    else:
        return sql_req
