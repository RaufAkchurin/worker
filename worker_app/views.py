from rest_framework import viewsets, generics

from worker_app.models import Category, Worker
from worker_app.serializers import ObjectSerializer, WorkTypeSerializer, WorkerSerializer
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


class ObjectListViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()


class CategoryListView(APIView):
    def get(self, request, object_id):
        try:
            # Получаем объект по айди
            object_instance = Object.objects.get(id=object_id)

            # Получаем все виды работ для данного объекта
            categories = Category.objects.filter(object=object_instance)

            # Получаем уникальные категории с айди и названием
            unique_categories = categories.values('id', 'name').distinct()

            # Преобразуем каждую категорию в словарь
            categories_list = [{'id': category['id'], 'name': category['name']} for category in
                               unique_categories]

            return Response({'categories': categories_list})

        except Object.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)


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
    serializer_class = WorkTypeSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return WorkType.objects.filter(category__id=category_id)


class ShiftCreationView(APIView):
    def post(self, request):
        serializer = ShiftCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
