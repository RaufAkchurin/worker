from django.urls import path

from worker_app.views import CategoryCreateView

urlpatterns = [
    path('category', CategoryCreateView.as_view(), name='category'),
]

