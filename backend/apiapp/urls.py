from django.urls import path
from apiapp.views import PlayerUsernameView, PlayerLastNameView, \
    PlayerFirstNameView , PlayerInfoView , PlayerAvatarView    


urlpatterns = [
    path('player/', PlayerInfoView.as_view(), name='playerView'),
    path('player/username', PlayerUsernameView.as_view(), name='playerUsernameView'),
    path('player/first_name', PlayerFirstNameView.as_view(), name='playerFirstNameView'),
    path('player/last_name', PlayerLastNameView.as_view(), name='playerLastNameView'),
    path('player/avatar', PlayerAvatarView.as_view(), name='playerAvatarView'),
    # path('player/avatar/update', update_avatar, name='postAvatar'),
]