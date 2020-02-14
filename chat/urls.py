from django.urls import path

from . import views
from .views import Create_Room, Matching_finished, Delete_chatting, Re_match, Delete_contact

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.room, name='room'),
    path('create/', Create_Room, name='create_room'),
    path('match_finished/<int:pk>', Matching_finished, name='match_finished'),
    path('re_match/<int:pk>', Re_match, name='re_match'),
    path('delete_contact/<int:pk>', Delete_contact, name='delete_contact'),
    path('delete_chat/', Delete_chatting, name='create_room'),
]
