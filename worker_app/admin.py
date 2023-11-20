from django.contrib import admin
from django.contrib.admin import site

from worker_app.models import Worker, Category, WorkType, Object, Shift, Measurement


# вдминке в типы работ добавить фильтр по категориям


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "object",)
    list_filter = ("object",)
    search_fields = ("name",)


# Register your models here.
class WorkTypeAdmin(admin.ModelAdmin):
    raw_id_fields = ("category",)
    list_filter = ("category",)
    search_fields = ("name",)


class ShiftAdmin(admin.ModelAdmin):
    raw_id_fields = ("work_type",)


site.register(Worker)
site.register(Category, CategoryAdmin)
site.register(Measurement)
site.register(WorkType, WorkTypeAdmin)
site.register(Object)
site.register(Shift, ShiftAdmin)
