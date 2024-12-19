"""Фильтры для SQL запросов"""
from datetime import datetime


def sql_filters(sql_req):
    """Фильтры для SQL запроса"""
    return sql_req.filter(
        is_published=True,
        pub_date__date__lt=datetime.now(),
        category__is_published=True
    )
