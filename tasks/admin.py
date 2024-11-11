from django.contrib import admin

from .models import Task

# Registering a model for display in the admin panel
admin.site.register(Task)
