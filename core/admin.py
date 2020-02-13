from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
# Register your models here.
<<<<<<< Updated upstream
from core.models import *

#admin.site.register(Category)
admin.site.register(Posting)
<<<<<<< Updated upstream
admin.site.register(Tag)
# admin.site.register(Boards, BoardAdmin)
# admin.site.register(Store)

@admin.register(Store)
class StoreAdimin(ImportExportModelAdmin):
    pass