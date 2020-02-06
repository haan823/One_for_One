from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sms import views

urlpatterns = [
    path('send_sms/', views.send_sms, name="send_sms"),
    path('certificate_phone/', views.certificate_phone, name="cerfiticate_phone")
]