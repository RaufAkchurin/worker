from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    password = models.IntegerField()

    def __str__(self):
        return f"{self.surname} {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategorySub(models.Model):
    category = models.OneToOneField(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkType(models.Model):
    sub_category = models.OneToOneField(CategorySub, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255)
    workers = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='workers')
    price_for_worker = models.IntegerField()
    price_for_customer = models.IntegerField()
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT, related_name='work_types')
    work_scope = models.IntegerField()

    def __str__(self):
        return self.name


class Shift(models.Model):
    object = models.OneToOneField(Object, on_delete=models.PROTECT)
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT)
    date = models.DateField()
    work_type = models.OneToOneField(WorkType, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.worker.name} -- {self.date}"

