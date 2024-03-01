from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/matchmaking/<int:capacity>/', consumers.Matchmaking.as_asgi()),
    path('ws/matchmaking/<int:capacity>/<int:match_id>/', consumers.Matchmaking.as_asgi()),
]
