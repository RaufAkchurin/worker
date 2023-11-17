from django.urls import path

from worker_app.report_pandas import GenerateReportView
from worker_app.views import ObjectListViewSet, CategoryListView, WorkTypesByObjectView

urlpatterns = [

    # OBJECT

    path(
        "objects",
        ObjectListViewSet.as_view({
                                'get': 'list',
                                 # 'post': 'create',
                                 # 'put': 'update'
                                 }),
        name="objects",
    ),

    path('object/<int:object_id>/categories/', CategoryListView.as_view(), name='category-list'),
    path('work_types_by_object/<int:object_id>/', WorkTypesByObjectView.as_view(), name='work_types_by_object'),
    path('generate_report/<int:object_id>/', GenerateReportView.as_view(), name='generate_report')
]

