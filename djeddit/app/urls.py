from django.urls import path,include 
from . import views


extra_patterns = [
    path('<int:sub_id>/',views.get_posts_for_sub, name = 'get-posts'),
    path('post/<int:post_id>/', views.get_comments_for_post, name = 'get-comments'),
    #path('<int:num>/',views.random_view,name = 'random')
]


urlpatterns = [
    path('',views.index,name = 'index'),
    
    #Endpoints for specific sub and post
    path('sub/',include(extra_patterns)),

    path('home/',views.home,name = 'home'),
    path('logout/',views.logout_view,name = 'logout'),
    path('login/',views.login_view,name = 'login'),
    path('signup/',views.signup_view,name = 'signup'),
    #path('process-login',views.process_login_view,name = 'process-login'), 
    path('create-sub/',views.create_sub_view,name = 'create-sub'),
    path('profile/',views.profile_view,name = 'profile'),
    path('profile/dashboard/',views.profile_dashboard_view,name = 'profile-dashboard'),
    path('all/',views.all_subs_view,name = 'all-subs'),
    
]