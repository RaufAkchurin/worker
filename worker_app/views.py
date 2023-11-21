from rest_framework import viewsets, generics

from worker_app.models import Category, Worker
from worker_app.serializers import ObjectSerializer, WorkTypeSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Object
from rest_framework.response import Response


class WorkerListViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Worker.objects.all()


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


# для смены - если вводится тип-работ и дата  на которые уже есть запись -
# спросить хочет ли он перезаписать и просто изменять данные

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Object, WorkType


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
                # 'price_for_worker': work_type.price_for_worker,
                # 'price_for_customer': work_type.price_for_customer,
                # 'total_scope': work_type.total_scope,
                # 'measurement_type': work_type.measurement_type.name,
            }
            for work_type in work_types
        ]

        # Return the data as JSON response
        return JsonResponse({'work_types': work_types_data})


class WorkTypeListByCategory(generics.ListAPIView):
    serializer_class = WorkTypeSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return WorkType.objects.filter(category__id=category_id)
