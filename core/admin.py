from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
# Register your models here.
from core.models import Store, Category, Crawling

admin.site.register(Category)
admin.site.register(Store)

@admin.register(Crawling)
class CrwalingAdimin(ImportExportModelAdmin):
    pass