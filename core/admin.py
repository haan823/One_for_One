from django.contrib import admin
# Register your models here.
<<<<<<< Updated upstream
from core.models import *

# class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
#     pass
=======
<<<<<<< HEAD
from core.models import Store, Category, Posting
>>>>>>> Stashed changes

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Posting)
<<<<<<< Updated upstream
admin.site.register(Tag)
# admin.site.register(Boards, BoardAdmin)
=======
=======
from core.models import *

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Posting)
admin.site.register(Tag)
>>>>>>> KSH_POSTING
>>>>>>> Stashed changes
