from django.urls import path

from . import views
from .views import Create_Room

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.room, name='room'),
    path('create/', Create_Room, name='create_room'),
]
