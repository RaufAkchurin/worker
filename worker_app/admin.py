import os

from django.contrib.admin import site
from django.contrib import admin
from django.http import HttpResponse
import requests
from dotenv import load_dotenv
from rangefilter.filter import DateRangeFilter

from worker_app.models import Worker, Category, WorkType, Object, Shift, Measurement, WorkersBenefits, TravelBenefits, \
    Travel

load_dotenv()

LOCALHOST_IP = os.getenv('LOCALHOST_IP')


class ObjectAdmin(admin.ModelAdmin):
    actions = ['download_report_customer', 'download_report_worker']

    def download_report_customer(self, request, queryset):
        # Получаем айди выбранных объектов
        selected_id = queryset.values_list('id', flat=False)

        # Отправляем запрос на ваше API, передавая айди объектов
        response = requests.get(f"http://{LOCALHOST_IP}/api/v1/report_customer/{selected_id[0][0]}/")

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем HTTP-ответ для скачивания файла
            response = HttpResponse(response.content,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report_customer.xlsx'
            return response
        else:
            self.message_user(request, "Ошибка при скачивании отчета. Пожалуйста, повторите попытку.")

    def download_report_worker(self, request, queryset):
        # Получаем айди выбранных объектов
        selected_id = queryset.values_list('id', flat=False)

        # Отправляем запрос на ваше API, передавая айди объектов
        response = requests.get(f"http://{LOCALHOST_IP}/api/v1/report_worker_general/{selected_id[0][0]}/")

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Создаем HTTP-ответ для скачивания файла
            response = HttpResponse(response.content,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report_worker.xlsx'
            return response
        else:
            self.message_user(request, "Ошибка при скачивании отчета. Пожалуйста, повторите попытку.")

    download_report_customer.short_description = "Отчёт для заказчика скачать"
    download_report_worker.short_description = "Отчёт для рабочего скачать"


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "telegram_id")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "object",)
    list_filter = ("object",)
    search_fields = ("name",)


class WorkTypeAdmin(admin.ModelAdmin):
    raw_id_fields = ("category",)
    list_filter = ("category",)
    search_fields = ("name",)
    list_display = ("category", "name", "price_for_worker", "price_for_customer", "total_scope", "measurement",)


class ShiftAdmin(admin.ModelAdmin):
    raw_id_fields = ("work_type",)
    list_filter = ("work_type__category__object",
                   "worker",
                   ('date', DateRangeFilter),
                   "work_type",)
    search_fields = ("name",)
    list_display = ("worker", "date", "work_type", "value",)


class WorkersBenefitsAdmin(admin.ModelAdmin):
    list_filter = ("object",
                   "worker",
                   ('date', DateRangeFilter),)
    list_display = ('worker', 'object', 'paid_amount', 'date')


######################################### TRAVELS #########################################


class TravelBenefitsInline(admin.TabularInline):  # Только для отображения выплат внеутри категории командировки
    model = TravelBenefits
    extra = 1  # Количество дополнительных форм для добавления выплаты прямо в интерфейсе командировки


class TravelAdmin(admin.ModelAdmin):
    inlines = [TravelBenefitsInline]
    list_display = ("object", "worker", "rate", "date_start", "date_finish",)
    list_filter = ("worker", "object")


class TravelBenefitsAdmin(admin.ModelAdmin):
    list_display = ("travel", "paid_for_travel", "date")
    list_filter = ("travel__worker", "travel__object")


site.register(Worker, WorkerAdmin)
site.register(Measurement)
site.register(WorkType, WorkTypeAdmin)
site.register(Object, ObjectAdmin)
site.register(Category, CategoryAdmin)
site.register(Shift, ShiftAdmin)
site.register(WorkersBenefits, WorkersBenefitsAdmin)


site.register(Travel, TravelAdmin)
site.register(TravelBenefits, TravelBenefitsAdmin)
