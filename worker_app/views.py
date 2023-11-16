from rest_framework import viewsets
from rest_framework import generics
from .models import WorkType
from .serializers import WorkTypeSerializer

from worker_app.models import Category, Object
from worker_app.serializers import ObjectSerializer


class ObjectViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectSerializer
    queryset = Category.objects.all()


class WorkTypeListByObjectView(generics.ListAPIView):
    serializer_class = WorkTypeSerializer

    def get_queryset(self):
        object_id = self.kwargs['pk']
        return WorkType.objects.filter(object__id=object_id)



# для смены - если вводится тип-работ и дата  на которые уже есть запись -
# спросить хочет ли он перезаписать и просто изменять данные