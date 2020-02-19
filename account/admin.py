from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from account.models import Univ, Profile

# admin.site.register(Univ)

admin.site.register(Profile)

@admin.register(Univ)
class UnivAdimin(ImportExportModelAdmin):
    pass