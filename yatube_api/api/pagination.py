from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 200
    page_size_query_param = "limit"
    page_query_param = "offset"

    def paginate_queryset(self, queryset, request, view=None):
        if "limit" in request.query_params or "offset" in request.query_params:
            return super().paginate_queryset(queryset, request, view)
        return None
