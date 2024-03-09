from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tictactoe/play/<str:room_id>/<int:player_id>', consumers.TicTacToeGameConsumer.as_asgi()),
]