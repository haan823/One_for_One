from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
# Register your models here.
from core.models import *

#admin.site.register(Category)
admin.site.register(Posting)
admin.site.register(Tag)
# admin.site.register(Boards, BoardAdmin)
# admin.site.register(Store)

@admin.register(Store)
class StoreAdimin(ImportExportModelAdmin):
    pass