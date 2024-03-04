from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination

from worker_app.models import Category, Worker
from worker_app.serializers import ObjectSerializer, WorkTypeSerializer, WorkerSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Object, WorkType
from .serializers import WorkerRegistrationSerializer, ShiftCreationSerializer


class WorkerListViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class WorkerByTelegramIdView(View):
    serializer_class = WorkerSerializer

    def get(self, request, telegram_id):
        # Get the object or return a 404 error if not found
        worker = get_object_or_404(Worker, telegram_id=telegram_id)

        # Serialize the data for JsonResponse
        worker_data = {
            'id': worker.pk,
            'name': worker.name,
            'surname': worker.surname,
            'telephone': worker.telephone
        }

        return JsonResponse({'worker': worker_data})


class WorkerRegistrationView(APIView):
    def post(self, request):
        serializer = WorkerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class WorkTypeListByCategory(generics.ListAPIView):
    serializer_class = WorkTypeSerializer
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


class ShiftCreationView(APIView):
    def post(self, request):
        serializer = ShiftCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
