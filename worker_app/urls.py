from django.urls import path

from worker_app.report_customer import ReportCustomerView
from worker_app.report_worker import ReportWorkerView
from worker_app.views import ObjectListViewSet, CategoryListView, WorkTypesByObjectView, \
    WorkerListViewSet, WorkerByTelegramIdView, WorkerRegistrationView, ShiftCreationView, WorkTypeListByCategory, \
    WorkTypesCreateView, MeasurementListViewSet, LogCreationView

urlpatterns = [
    # WORKERS
    path("workers", WorkerListViewSet.as_view({'get': 'list', }), name="workers", ),
    path("worker_by_tg/<int:telegram_id>", WorkerByTelegramIdView.as_view(), name="worker_by_tg", ),
    path("worker_registration", WorkerRegistrationView.as_view(), name="worker_registration"),

    #  OBJECTS
    path("objects", ObjectListViewSet.as_view({'get': 'list', }), name="objects", ),
    path('object/<int:object_id>/categories/', CategoryListView.as_view({'get': 'list', }), name='object-categories'),

    #  WORK TYPES
    path('work_types/object/<int:object_id>/', WorkTypesByObjectView.as_view(), name='work_types_by_object'),
    path('work_types/category/<int:category_id>/', WorkTypeListByCategory.as_view(), name='work_types_by_category'),
    path("work_types/create", WorkTypesCreateView.as_view(), name="work_types_create"),

    # MEASUREMENT
    path("measurements", MeasurementListViewSet.as_view({'get': 'list', }), name="measurements", ),

    #  REPORTS
    path('report_customer/<int:object_id>/', ReportCustomerView.as_view(), name='report_customer'),
    path('report_worker_general/<int:object_id>/', ReportWorkerView.as_view(), name='report_worker_general'),
    path('report_worker_individual/<int:object_id>/<int:worker_id>/', ReportWorkerView.as_view(), name='report_worker_individual'),

    # SHIFT
    path("shift_creation", ShiftCreationView.as_view(), name="shift_creation"),

    # LOG
    path("log_creation", LogCreationView.as_view(), name="log_creation"),

]
