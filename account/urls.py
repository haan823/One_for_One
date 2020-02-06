from django.urls import path

from account.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', goto_signup, name='goto_signup'),
    path('signup/<int:pk>/', signup, name='signup'),
    path('active/<token>', user_active, name='user_active'),
]