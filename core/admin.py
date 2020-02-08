from django.contrib import admin

# Register your models here.
from core.models import Store, Category, Location

admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Store)