from rest_framework import serializers

from worker_app.models import Category, CategorySub, Object


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySubSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySub
        fields = '__all__'