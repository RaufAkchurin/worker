from rest_framework import serializers

from worker_app.models import Category, Object, WorkType, Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "id",
            "name",
        )


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
        fields = (
            "id",
            "name",
        )
