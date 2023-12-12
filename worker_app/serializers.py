from rest_framework import serializers

from worker_app.models import Category, Object, WorkType, Worker, Measurement, Shift


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


class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = (
            "id",
            "name",
        )


class WorkTypeSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer(source="measurement_type")

    class Meta:
        model = WorkType
        fields = (
            "id",
            "name",
            "measurement",
        )


class ShiftCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = (
            "worker",
            "date",
            "work_type",
            "value",
        )



