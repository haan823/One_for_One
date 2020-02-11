from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('new/<int:pk>/', views.match_new, name='match_new'),
    # path('new/choice/', views.store_choice, name='store_choice'),
]