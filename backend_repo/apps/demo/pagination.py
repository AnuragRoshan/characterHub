from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to exclude count, next, and previous fields.
    """
    page_size = 10  # Default page size

    def get_paginated_response(self, data):
        return Response({
            'data': data  # Only return the results
        })
