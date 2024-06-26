from django.urls import path
from . import views



urlpatterns = [
    path('', views.getroute),
    path('spaces/', views.getspaces),
    path('spaces/<str:pk>', views.getspace),
]
