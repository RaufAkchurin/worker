

from django.contrib import admin
from django.contrib.admin import site

from worker_app.models import User, Object, WorkCategory

# Register your models here.
site.register(User)
site.register(Object)
site.register(WorkCategory)
