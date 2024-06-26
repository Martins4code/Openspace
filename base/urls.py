from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home" ),
    path('space/<str:pk>/', views.space, name="space"),
    path('create-space/', views.create_space, name= "create-space"),
     path('profile/<str:pk>/', views.user_profile, name= "user-profile"),
    path('update-space/<str:pk>', views.update_space, name= "update-space"),
    path('delete-space/<str:pk>', views.delete_space, name= "delete-space"),
    path('delete-message/<str:pk>', views.delete_message, name= "delete-message"),
    path('login/', views.login_page, name= "login"),
    path('logout_/', views.logoutUser, name= "logout"),
    path('register/', views.register_page, name= "register"),
    
    path('update-user/', views.UpdateUser, name= "update-user"),
    path('topics/', views.topics_page, name= "topics"),
    path('activity/', views.activity_page, name= "activity"),
]
