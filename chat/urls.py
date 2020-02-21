from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.room, name='room'),
    path('create/<int:pk>', views.create_Room, name='create_room'),
    path('room_finished/<int:pk>', views.room_finished, name='room_finished'),
    path('review/<int:pk>/', views.review, name='review'),
    path('review/update/<int:pk>/', views.update_review, name='update_review'),
    path('delete_contact/<int:pk>', views.delete_contact, name='delete_contact'),
]
