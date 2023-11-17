from django.urls import path

from worker_app.report_pandas import GenerateReportView
from worker_app.views import ObjectListViewSet, CategoryListView

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
    path('generate_report/', GenerateReportView.as_view(), name='generate_report')
]

