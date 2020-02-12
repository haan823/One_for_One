from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Posting)
admin.site.register(Tag)