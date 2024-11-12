from django.contrib import admin
from .models import Comment

# Registering a model for display in the admin panel
admin.site.register(Comment)
