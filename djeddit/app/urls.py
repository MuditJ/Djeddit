from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('home',views.home,name = 'home'),
    path('logout',views.logout_view,name = 'logout'),
]