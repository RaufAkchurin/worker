from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        prev_url = self.get_previous_link()

        # Cut base URL
        base_url = self.request.build_absolute_uri('/')
        next_url_cut = next_url.replace(base_url, '') if next_url else None
        prev_url_cut = prev_url.replace(base_url, '') if prev_url else None

        return Response({
            'count': self.page.paginator.count,
            'next': next_url_cut,
            'previous': prev_url_cut,
            'results': data
        })
