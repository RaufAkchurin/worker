from rest_framework import status, viewsets

from worker_app.models import Category, CategorySub, Object
from worker_app.serializers import CategorySerializer, CategorySubSerializer, ObjectSerializer


class ObjectViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategorySubViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySubSerializer
    queryset = CategorySub.objects.all()
