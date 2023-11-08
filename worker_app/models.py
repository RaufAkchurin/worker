from django.db import models

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    password = models.IntegerField()


class WorkCategory(models.Model):
    name = models.CharField(max_length=10)


class WorkType(models.Model):
    name = models.CharField(max_length=10)
    category = models.ForeignKey(model=WorkCategory)
    measurement = models.CharField(max_length=3)


class Object(models.Model):
    name = models.CharField(max_length=10)
    workers = models.ForeignKey(model=User)
    price_for_worker = models.IntegerField()
    price_for_customer = models.IntegerField()
    work_type = models.ForeignKey(model=WorkType)
    work_scope = models.IntegerField()
