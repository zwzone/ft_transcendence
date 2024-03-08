from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('tictactoe/ws/', consumers.TicTacToeGameConsumer.as_asgi()),
]