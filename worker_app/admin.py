from django.contrib.admin import site
from django.contrib import admin
from django.http import HttpResponse
import requests
from rangefilter.filter import DateRangeFilter

from worker_app.models import Worker, Category, WorkType, Object, Shift, Measurement, WorkersBenefits


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "object",)
    list_filter = ("object",)
    search_fields = ("name",)


class WorkTypeAdmin(admin.ModelAdmin):
    raw_id_fields = ("category",)
    list_filter = ("category",)
    search_fields = ("name",)


class ShiftAdmin(admin.ModelAdmin):
    raw_id_fields = ("work_type",)
    list_filter = ("work_type__category__object",
                   "worker",
                   ('date', DateRangeFilter),
                   "work_type",)
    search_fields = ("name",)


class WorkersBenefitsAdmin(admin.ModelAdmin):
    list_filter = ("object",
                   "worker",
                   ('date', DateRangeFilter),)


class ObjectAdmin(admin.ModelAdmin):
    actions = ['download_report']

    def download_report(self, request, queryset):
        # Получаем айди выбранных объектов
        selected_id = queryset.values_list('id', flat=False)

        # TODO использовать реверс для построения ссылки для скачивания отчёта

        # Отправляем запрос на ваше API, передавая айди объектов
        response = requests.get(f"http://127.0.0.1:8000/api/v1/report_customer/{selected_id[0][0]}/")

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем HTTP-ответ для скачивания файла
            response = HttpResponse(response.content,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            return response
        else:
            self.message_user(request, "Ошибка при скачивании отчета. Пожалуйста, повторите попытку.")

    download_report.short_description = "Отчёт для заказчика скачать"


site.register(Worker)
site.register(Category, CategoryAdmin)
site.register(Measurement)
site.register(WorkType, WorkTypeAdmin)
site.register(Object, ObjectAdmin)
site.register(Shift, ShiftAdmin)
site.register(WorkersBenefits, WorkersBenefitsAdmin)
