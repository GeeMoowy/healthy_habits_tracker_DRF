from rest_framework.pagination import PageNumberPagination


class HabitsPagination(PageNumberPagination):
    """Кастомная пагинация для списка привычек.
    Добавляет:
    - Стандартный размер страницы (5 элементов)
    - Поддержку динамического изменения размера страницы через параметр URL
    - Ограничение максимального размера страницы (100 элементов)"""

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
