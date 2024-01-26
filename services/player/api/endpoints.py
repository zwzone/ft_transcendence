from django.urls import path
from .views import (
    PlayerUsernameView,
    PlayerLastNameView,
    PlayerFirstNameView,
    PlayerInfoView,
    PlayerAvatarView,
    PlayerAddFriend,
)

urlpatterns = [
    path('', PlayerInfoView.as_view(), name='playerView'),
    path('username/', PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('first_name/', PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('last_name/', PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('avatar/', PlayerAvatarView.as_view(), name='playerAvatarView'),
    path('add_friend/', PlayerAddFriend.as_view(), name='playerAddFriendView'),
]
