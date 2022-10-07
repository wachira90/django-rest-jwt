from django.contrib import admin

# Register your models here.
from .models import Task

# Register our model
admin.site.register(Task)