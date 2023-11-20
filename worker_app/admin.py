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
    list_filter = ("work_type",)
    search_fields = ("name",)

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
import requests


class ObjectAdmin(admin.ModelAdmin):
    actions = ['download_report']

    def download_report(self, request, queryset):
        # Получаем айди выбранных объектов
        selected_id = queryset.values_list('id', flat=False)

        # Отправляем запрос на ваше API, передавая айди объектов
        api_url = reverse('generate_report')  # Замените 'your_api_endpoint' на реальный endpoint вашего API
        response = requests.get(api_url, params={'object_id': selected_id})

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем HTTP-ответ для скачивания файла
            response = HttpResponse(response.content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            return response
        else:
            self.message_user(request, "Ошибка при скачивании отчета. Пожалуйста, повторите попытку.")

    download_report.short_description = "Скачать отчет"


site.register(Worker)
site.register(Category, CategoryAdmin)
site.register(Measurement)
site.register(WorkType, WorkTypeAdmin)
site.register(Object, ObjectAdmin)
site.register(Shift, ShiftAdmin)
