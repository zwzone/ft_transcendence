from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerView.as_view(), name='playerView'),
    path('add_friend/', views.PlayerAddFriend.as_view(), name='playerAddFriendView'),
]
