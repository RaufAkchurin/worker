from django.contrib import admin
from django.contrib.admin import site

from worker_app.models import Worker, Category, WorkType, Object, Shift, Measurement

# Register your models here.

site.register(Worker)
site.register(Category)
site.register(Measurement)
site.register(WorkType)
site.register(Object)
site.register(Shift)
