from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('home/<int:pk>', views.home, name='home'),
    path('new/', views.match_new, name='match_new'),
    # path('cat/<int:pk>/', views.choice_cat, name='choice_cat'),
    # path('cat/<int:pk>/store/', views.choice_store, name='choice_store'),
    path('new/fin/', views.match_fin, name='match_fin'),
    path('my_page/', views.my_page, name='my_page'),
    path('search/', views.search, name='search'),
    path('search_store/', views.search_store, name='search_store'),
    path('new/cat/', views.choice_cat, name='choice_cat'),
    path('new/detail/', views.choice_detail, name='choice_detail'),
    # path('new/choice/', views.test_choice, name='test_choice'),
    path('new/test/', views.new_test, name='new_test'),
]
