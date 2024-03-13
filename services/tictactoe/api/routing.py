from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tictactoe/', consumers.TicTacToeGameConsumer.as_asgi()),
]