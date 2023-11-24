from django.urls import path

from worker_app.report_customer import ReportCustomerView
from worker_app.report_worker import ReportWorkerView
from worker_app.views import ObjectListViewSet, CategoryListView, WorkTypesByObjectView, WorkTypeListByCategory, \
    WorkerListViewSet

urlpatterns = [
    path("workers", WorkerListViewSet.as_view({'get': 'list', }), name="workers", ),

    #  OBJECTS
    path("objects", ObjectListViewSet.as_view({'get': 'list', }), name="objects", ),
    path('object/<int:object_id>/categories/', CategoryListView.as_view(), name='object-categories'),

    #  WORK TYPES
    path('work_types/object/<int:object_id>/', WorkTypesByObjectView.as_view(), name='work_types_by_object'),
    path('work_types/category/<int:category_id>/', WorkTypeListByCategory.as_view(), name='work_types_by_category'),

    #  REPORTS
    path('report_customer/<int:object_id>/', ReportCustomerView.as_view(), name='report_customer'),
    path('report_worker/<int:object_id>/', ReportWorkerView.as_view(), name='report_worker'),

]
