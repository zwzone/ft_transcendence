from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/pong/<str:room_id>/<int:capacity>/', consumers.Pong.as_asgi()),
]