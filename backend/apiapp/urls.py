from django.urls import path

from apiapp.views import player_api, get_user_by_username, update_username, get_avatar, update_avatar

urlpatterns = [
    path('player/', player_api, name='playerView'),
    path('player/<str:username>/', get_user_by_username, name='getPlayerByUsername'),
    path('player/UpdateUsername', update_username, name='postUsername'),
    path('player/avatar', get_avatar, name='getAvatar'),
    path('player/avatar/Update', update_avatar, name='postAvatar'),
]