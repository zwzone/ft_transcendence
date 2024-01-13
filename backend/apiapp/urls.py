from django.urls import path

from apiapp.views import player_api, get_user_by_username

urlpatterns = [
    path('player/', player_api, name='playerView'),
    path('player/<str:username>/', get_user_by_username, name='getPlayerByUsername'),
]