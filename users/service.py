from django.core.paginator import Paginator

from team_finder import constants


def get_paginated_objects(request, queryset, page_size=constants.PAGINATION_PAGE_SIZE):
    """
    Вспомогательная функция для пагинации объектов.
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
