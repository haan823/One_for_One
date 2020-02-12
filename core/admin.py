from django.contrib import admin
from import_export.admin import ImportExportMixin, ImportMixin
# Register your models here.
from core.models import *

class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Posting)
admin.site.register(Tag)
admin.site.register(Boards, BoardAdmin)