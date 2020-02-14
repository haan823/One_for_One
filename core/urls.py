from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.main, name='main'),
    path('home/<int:pk>', views.home, name='home'),
    path('new/', views.match_new, name='match_new'),
    path('cat/<int:pk>/', views.choice_cat, name='choice_cat'),
    path('cat/<int:pk>/store/', views.choice_store, name='choice_store'),
    path('new/fin/', views.match_fin, name='match_fin'),
    path('mypage/', views.mypage, name='mypage'),
    path('test/', views.test, name='test'),
    path('test/cat', views.test_cat, name='test_cat'),
    # path('polls/', views.upload, name='upload'),
    # path('import/', views.simple_upload, name='simple_upload')
]
