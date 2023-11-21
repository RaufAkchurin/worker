from django.urls import path

from worker_app.report_pandas import GenerateReportView
from worker_app.views import ObjectListViewSet, CategoryListView, WorkTypesByObjectView, WorkTypeListByCategory, \
    WorkerListViewSet

urlpatterns = [
    path("workers", WorkerListViewSet.as_view({'get': 'list', }), name="workers",),

    path("objects", ObjectListViewSet.as_view({'get': 'list', }), name="objects",),
    path('object/<int:object_id>/categories/', CategoryListView.as_view(), name='category-list'),

    path('work_types_by_object/<int:object_id>/', WorkTypesByObjectView.as_view(), name='work_types_by_object'),
    path('worktypes/category/<int:category_id>/', WorkTypeListByCategory.as_view(), name='worktype-list-by-category'),

    path('generate_report/<int:object_id>/', GenerateReportView.as_view(), name='generate_report'),

]
