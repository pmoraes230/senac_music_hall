from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('user_register/', views.user, name='user_register'),
    path('events_register/', views.event_register, name='events_register'),
    path('building_register/', views.building_register, name='building_register')
]
