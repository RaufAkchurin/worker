from django.contrib.admin import site

from worker_app.models import Worker, Category, CategorySub, WorkType, Object, Shift

# Register your models here.
site.register(Worker)
site.register(Category)
site.register(CategorySub)
site.register(WorkType)
site.register(Object)
site.register(Shift)
