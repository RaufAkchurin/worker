from rest_framework import serializers

from worker_app.models import Category, Object, WorkType, Worker, Measurement, Shift, Log


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = (
            "id",
            "name",
            "surname"
        )


class WorkerRegistrationSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(required=True)

    class Meta:
        model = Worker
        fields = (
            "name",
            "surname",
            "telephone",
            "telegram_id"
        )


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = (
            "id",
            "name",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id",
            "name",
        )


class ShiftCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = (
            "worker",
            "date",
            "work_type",
            "value",
        )


class LogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            "func",
            "description",
            "created_at",
        )


class WorkTypeViewSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer()

    class Meta:
        model = WorkType
        fields = (
            "id",
            "name",
            "measurement",
        )


class WorkTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = (
            "category",
            "name",
            "measurement",
            "created_by"
        )
