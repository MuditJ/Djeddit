from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('home',views.home,name = 'home'),
    path('logout',views.logout_view,name = 'logout'),
    path('login',views.login_view,name = 'login'),
    #path('process-login',views.process_login_view,name = 'process-login'), 
    path('create-sub',views.create_sub_view,name = 'create-sub'),
]