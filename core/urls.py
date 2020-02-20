from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('home/<int:pk>/', views.home, name='home'),
    path('new/', views.match_new, name='match_new'),
    path('new/fin/', views.match_fin, name='match_fin'),
    path('my_page/', views.my_page, name='my_page'),
    path('new/detail/', views.choice_detail, name='choice_detail'),
    path('match_request/<int:pk>', views.match_request, name='match_request'),
    path('accept/<int:pk>', views.accept, name='accept'),
    path('refuse/<int:pk>', views.refuse, name='refuse'),
    path('search/', views.search, name='search'),
    path('search_store/', views.search_store, name='search_store'),
    path('delete/<int:pk>', views.delete_posting, name='delete_posting')

]
