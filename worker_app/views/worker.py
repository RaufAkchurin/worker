from rest_framework import viewsets
from worker_app.models import Category, Worker, Measurement
from worker_app.serializers import ObjectSerializer, WorkTypeViewSerializer, WorkerSerializer, CategorySerializer, \
    WorkTypeCreateSerializer, MeasurementSerializer, LogCreateSerializer, WorkerRegistrationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View


# WORKER VIEWS
class WorkerListViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class WorkerByTelegramIdView(View):
    serializer_class = WorkerSerializer

    def get(self, request, telegram_id):
        # Get the object or return a 404 error if not found
        worker = get_object_or_404(Worker, telegram_id=telegram_id)

        # Serialize the data for JsonResponse
        worker_data = {
            'id': worker.pk,
            'name': worker.name,
            'surname': worker.surname,
            'telephone': worker.telephone
        }

        return JsonResponse({'worker': worker_data})


class WorkerRegistrationView(APIView):
    def post(self, request):
        serializer = WorkerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
