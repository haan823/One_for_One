from django.contrib import admin

# Register your models here.
from account.models import Univ, Profile

admin.site.register(Univ)

admin.site.register(Profile)