from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    password = models.IntegerField()

    def __str__(self):
        return self.name


class WorkCategory(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class WorkType(models.Model):
    name = models.CharField(max_length=10)
    category = models.ForeignKey(model=WorkCategory, on_delete=models.CASCADE)
    value_type = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=10)
    workers = models.ForeignKey(model=Worker, on_delete=models.CASCADE)
    price_for_worker = models.IntegerField()
    price_for_customer = models.IntegerField()
    work_type = models.ForeignKey(model=WorkType)
    work_scope = models.IntegerField()

    def __str__(self):
        return self.name


class Work_shift(models.Model):
    worker = models.ForeignKey(model=Worker, on_delete=models.PROTECT)
    date = models.DateField()
    work_type = models.OneToOneField(model=WorkType, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.worker.name} -- {self.date}"

