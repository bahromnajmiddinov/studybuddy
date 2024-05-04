from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path("profile/<str:pk>/", views.profile, name="profile"),
    path('edit-profile/', views.editProfile, name='editProfile'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('topics/', views.topics, name='topics'),
    path('activities/', views.activities, name='activities'),
]
