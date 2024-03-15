from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from worker_app.models import Category, Worker, Measurement, Object, WorkType
from worker_app.serializers import ObjectSerializer, WorkTypeViewSerializer, WorkerSerializer, CategorySerializer, \
    WorkTypeCreateSerializer, MeasurementSerializer, LogCreateSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View

from worker_app.views.utils import CustomPageNumberPagination


# WORK TYPES VIEWS
class WorkTypesByObjectView(View):
    def get(self, request, object_id):
        # Get the object or return a 404 error if not found
        obj = get_object_or_404(Object, id=object_id)

        # Get all work types related to the specified object
        work_types = WorkType.objects.filter(category__object=obj)

        # Serialize the data for JsonResponse
        work_types_data = [
            {
                'id': work_type.pk,
                'name': work_type.name,
            }
            for work_type in work_types
        ]

        return JsonResponse({'work_types': work_types_data})


class WorkTypeListByCategory(generics.ListAPIView):
    serializer_class = WorkTypeViewSerializer
    pagination_class = CustomPageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return WorkType.objects.filter(category__id=category_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WorkTypesCreateView(APIView):
    def post(self, request):
        serializer = WorkTypeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
