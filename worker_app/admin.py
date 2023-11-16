from django.contrib import admin
from django.contrib.admin import site

from worker_app.models import Worker, Category, WorkType, Object, Shift, Measurement


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "object",)
    list_filter = ("object", )
    search_fields = ("name",)


# Register your models here.
class WorkTypeAdmin(admin.ModelAdmin):
    raw_id_fields = ("category",)



site.register(Worker)
site.register(Category, CategoryAdmin)
site.register(Measurement)
site.register(WorkType, WorkTypeAdmin)
site.register(Object)
site.register(Shift)
