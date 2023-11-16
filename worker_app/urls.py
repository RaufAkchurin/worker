from django.urls import path

from worker_app.views import  ObjectViewSet, WorkTypeListByObjectView

urlpatterns = [

    # OBJECT

    path(
        "object",
        ObjectViewSet.as_view({
                                'get': 'list',
                                 # 'post': 'create',
                                 # 'put': 'update'
                                 }),
        name="object",
    ),
    # path('omac/type/<int:pk>/', TypeView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),

    path('work_types/<int:pk>/', WorkTypeListByObjectView.as_view(), name='worktype-list-by-object')


]

