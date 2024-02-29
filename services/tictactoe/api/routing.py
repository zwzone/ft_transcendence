from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/match/', consumers.TicTacToeConsumer.as_asgi()),
]