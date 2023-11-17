from rest_framework import viewsets

from worker_app.models import Category
from worker_app.serializers import ObjectSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Object
from rest_framework.response import Response

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


