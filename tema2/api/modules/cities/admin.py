from django.contrib import admin
from .models import City

# Register the model in the Admin View, for a very intuitive DB manipulation
# tool, built-in in Django
admin.site.register(City)
