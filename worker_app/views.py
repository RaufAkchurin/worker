from rest_framework import viewsets

from worker_app.models import Category, Object
from worker_app.serializers import ObjectSerializer


class ObjectListViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Object, WorkType


class CategoryListView(APIView):
    def get(self, request, object_id):
        try:
            # Получаем объект по айди
            object_instance = Object.objects.get(id=object_id)

            # Получаем все виды работ для данного объекта
            work_types = WorkType.objects.filter(object=object_instance)

            # Получаем уникальные категории с айди и названием
            unique_categories = work_types.values('category__id', 'category__name').distinct()

            # Преобразуем каждую категорию в словарь
            categories_list = [{'id': category['category__id'], 'name': category['category__name']} for category in unique_categories]

            return Response({'categories': categories_list})

        except Object.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)



# для смены - если вводится тип-работ и дата  на которые уже есть запись -
# спросить хочет ли он перезаписать и просто изменять данные