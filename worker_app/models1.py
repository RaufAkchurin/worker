from django.db import models

from worker_app.models import Worker, WorkType


class Object(models.Model):
    name = models.CharField(max_length=255)
    workers = models.ManyToManyField(Worker)
    work_types = models.ManyToManyField(WorkType)

    def __str__(self):
        return self.name