from rest_framework import viewsets

from worker_app.models import Category, Object
from worker_app.serializers import ObjectSerializer


class ObjectListViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()


from rest_framework.views import APIView
from rest_framework import status
from .models import Object, WorkType


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


from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from .models import Shift
import os

# @api_view(['GET'])
# def generate_report(request):
#     shifts = Shift.objects.all()
#
#     # Создайте DataFrame из данных модели Shift
#     data = {
#         'Object': [shift.object.name for shift in shifts],
#         'Worker Surname': [shift.worker.surname for shift in shifts],
#         'Worker Name': [shift.worker.name for shift in shifts],
#         'Date': [shift.date for shift in shifts],
#         'Work Type': [shift.work_type.name for shift in shifts],
#         'Value': [shift.value for shift in shifts],
#     }
#     df = pd.DataFrame(data)
#
#     # Сохраните DataFrame в Excel в корневой директории
#     excel_path = 'shift_report.xlsx'
#     df.to_excel(excel_path, index=False)
#
#     # Создайте BytesIO объект для отправки файла Excel в HttpResponse
#     excel_file = BytesIO()
#     df.to_excel(excel_file, index=False)
#     excel_file.seek(0)
#
#     # Создайте HttpResponse для отправки файла Excel
#     response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = f'attachment; filename={excel_path}'
#
#     return response

