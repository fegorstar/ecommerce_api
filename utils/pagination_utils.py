from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

class CustomPagination(PageNumberPagination):
    """
    Custom pagination for API responses.
    """
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Query param to set the page size dynamically
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        """
        Override the paginated response to follow the standard format.
        """
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Products retrieved successfully",  # Match test expectations
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            },
            status=status.HTTP_200_OK
        )
