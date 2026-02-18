from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на странице по умолчанию
    page_size_query_param = "page_size"  # Позволяет клиенту менять размер страницы через параметр запроса (опционально)
    max_page_size = 100  # Максимальный размер страницы (ограничение)
