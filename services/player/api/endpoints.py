from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerInfo.as_view(), name='playerInfoView'),
    path('avatar/', views.PlayerAvatarUpload.as_view(), name='playerAvatarUploadView'),
    path('add_friend/', views.PlayerAddFriend.as_view(), name='playerAddFriendView'),
]
