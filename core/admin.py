from django.contrib import admin

# Register your models here.
from core.models import Store, Category, Univ

admin.site.register(Univ)
admin.site.register(Category)
admin.site.register(Store)