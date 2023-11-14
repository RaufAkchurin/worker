from django.urls import path

from worker_app.views import CategoryViewSet, CategorySubViewSet, ObjectViewSet

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


    # CATEGORY
    # path('category', CategoryViewSet.as_view(), name='category'),
    path(
        "category",
        CategoryViewSet.as_view({
                                'get': 'list',
                                 # 'post': 'create',
                                 # 'put': 'update'
                                 }),
        name="category",
    ),
    # path('omac/type/<int:pk>/', TypeView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),

    #CATEGORY SUB
    # path('category', CategoryViewSet.as_view(), name='category'),
    path(
        "category_sub",
        CategorySubViewSet.as_view({
            'get': 'list',
            # 'post': 'create',
            # 'put': 'update'
        }),
        name="category_sub",
    ),
    # path('omac/type/<int:pk>/', TypeView.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),


]

