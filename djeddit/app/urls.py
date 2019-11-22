from django.urls import path,include 
from . import views


extra_patterns = [
    path('<int:sub_id>/',views.get_posts_for_sub, name = 'get-posts'),
    path('<int:sub_id>/dashboard/',views.sub_dashboard_view,name = 'sub-dashboard'),
    path('post/<int:post_id>/', views.get_comments_for_post, name = 'get-comments'),
    #path('post/<int:post_id>/sentiment/',views.get_post_sentiment,name = 'post-sentiment'), 
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
    path('create-post/',views.create_post_view,name = 'create-post'),
    path('create-comment/',views.create_comment_view, name = 'create-comment'),
    path('profile/',views.profile_view,name = 'profile'),
    #path('profile/dashboard/',views.profile_dashboard_view,name = 'profile-dashboard'),
    #path('get-chart-data/',views.get_chart_view,name = 'get-chart'),
    path('all/',views.all_subs_view,name = 'all-subs'),
    path('random/',views.random_view,name = 'random'),
    path('profile/dashboard/',views.profile_dashboard_view,name = 'dashboard'),
    path('api/data/<int:sub_id>/', views.sub_dashboard_data, name = 'json-sub-data'),
    path('api/data/',views.get_chart_view,name = 'json-data'),
    
]