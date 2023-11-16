from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    password = models.IntegerField()
    telegram_id = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"{self.surname} {self.name}"


class Measurement(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    price_for_worker = models.IntegerField()
    price_for_customer = models.IntegerField()
    total_scope = models.IntegerField()
    measurement_type = models.ForeignKey(Measurement, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255)
    # workers = models.ManyToManyField(Worker)
    categories = models.ManyToManyField(Category, blank=True)
    work_types = models.ManyToManyField(WorkType, blank=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField()
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.worker.name} -- {self.date}"

