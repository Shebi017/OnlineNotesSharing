from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('user_signup/',views.user_signup,name="user_signup"),
    path('user_login/',views.user_login,name="user_login"),
    path('admin_login/',views.admin_login,name="admin_login"),
    
    path('profile_home/',views.profile_home,name="profile_home"),
    path('view_all/',views.view_all_notes,name="view_all"),
    path('view_my/',views.view_my_notes,name="view_my"),
    path('upload_notes/',views.upload_notes,name="upload_notes"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('change_password/',views.change_password,name="change_password"),




]