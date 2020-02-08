from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sms import views

app_name = "sms"

urlpatterns = [
    path('send_sms/', views.send_sms, name="send_sms"),
    path('certificate_phone/', views.certificate_phone, name="certificate_phone"),
    path('certificate_phone_done', views.certificate_phone_done, name="certificate_phone_done")
]