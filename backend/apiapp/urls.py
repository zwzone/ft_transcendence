from django.urls import path

from apiapp.views import player_api

urlpatterns = [
    path('player/', player_api, name='playerView'),
]
