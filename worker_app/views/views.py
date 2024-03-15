from rest_framework import viewsets, generics

from worker_app.models import Category, Measurement
from worker_app.serializers import ObjectSerializer, WorkTypeViewSerializer, CategorySerializer, \
    MeasurementSerializer, LogCreateSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from worker_app.views.utils import CustomPageNumberPagination
from worker_app.models import Object, WorkType
from worker_app.serializers import ShiftCreateSerializer


class ObjectListViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    pagination_class = CustomPageNumberPagination
    pagination_class.page_size = 10

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryListView(viewsets.ModelViewSet):
    # page size depended from page size WorkTypeListByCategory and i don't known why
    serializer_class = CategorySerializer  # Replace with your actual serializer class
    pagination_class = CustomPageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        object_id = self.kwargs.get('object_id')
        try:
            object_instance = Object.objects.get(id=object_id)
            categories = Category.objects.filter(object=object_instance).distinct()
            return categories
        except Object.DoesNotExist:
            return Category.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MeasurementListViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all().order_by('id')
    pagination_class = CustomPageNumberPagination
    pagination_class.page_size = 10

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShiftCreationView(APIView):
    def post(self, request):
        serializer = ShiftCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogCreationView(APIView):
    def post(self, request):
        serializer = LogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
