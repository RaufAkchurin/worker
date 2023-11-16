from rest_framework import serializers

from worker_app.models import Category, Object, WorkType


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = (
            "id",
            "name",
        )


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'
