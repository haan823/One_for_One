from django.contrib import admin
# from import_export.admin import ExportActionModelAdmin
# Register your models here.
from core.models import Store, Category

# class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
#     pass

admin.site.register(Category)
admin.site.register(Store)
# admin.stie.register(Boards, BoardAdmin)