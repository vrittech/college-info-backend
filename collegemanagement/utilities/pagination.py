from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 5000

    def get_paginated_response(self, data):
        """
        Override the default paginated response to ensure the structure remains correct.
        """
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
