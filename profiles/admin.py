from django.contrib import admin
from .models import Profile

# Registering a model for display in the admin panel
admin.site.register(Profile)